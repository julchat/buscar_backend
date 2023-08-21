import matplotlib.pyplot as plt
import xml.dom.minidom
import time
import random
import numpy as np
from six import BytesIO
from PIL import Image

import errno
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from IPython.display import Image as IPyImage

import tensorflow as tf

from object_detection.utils import config_util
from object_detection.utils import visualization_utils as viz_utils
from object_detection.builders import model_builder


def load_image_into_numpy_array(path):
    """Load an image from file into a numpy array.

    Puts image into numpy array to feed into tensorflow graph.
    Note that by convention we put it into a numpy array with shape
    (height, width, channels), where channels=3 for RGB.

    Args:
        path: a file path.

    Returns:
        uint8 numpy array with shape (img_height, img_width, 3)
    """
    img_data = tf.io.gfile.GFile(path, 'rb').read()
    image = Image.open(BytesIO(img_data))
    (im_width, im_height) = image.size
    return np.array(image.getdata()).reshape(
        (im_height, im_width, 3)).astype(np.uint8)


def plot_detections(image_np,
                    boxes,
                    classes,
                    scores,
                    category_index,
                    figsize=(12, 16),
                    image_name=None):
    """Wrapper function to visualize detections.

    Args:
        image_np: uint8 numpy array with shape (img_height, img_width, 3)
        boxes: a numpy array of shape [N, 4]
        classes: a numpy array of shape [N]. Note that class indices are 1-based,
        and match the keys in the label map.
        scores: a numpy array of shape [N] or None.  If scores=None, then
        this function assumes that the boxes to be plotted are groundtruth
        boxes and plot all boxes as black with no classes or scores.
        category_index: a dict containing category dictionaries (each holding
        category index `id` and category name `name`) keyed by category indices.
        figsize: size for the figure.
        image_name: a name for the image file.
    """
    image_np_with_annotations = image_np.copy()
    viz_utils.visualize_boxes_and_labels_on_image_array(
        image_np_with_annotations,
        boxes,
        classes,
        scores,
        category_index,
        use_normalized_coordinates=True,
        min_score_thresh=0.5)
    if image_name:
        plt.imsave(image_name, image_np_with_annotations)
    else:
        plt.imshow(image_np_with_annotations)


def xml_to_box_numpy_array(xml_path):
    dom = xml.dom.minidom.parse(xml_path)
    root = dom.documentElement

    # Descomentar si hay mas de un box y hacer un for, no es nuestro caso
    # objects=dom.getElementsByTagName("object")

    bndbox = root.getElementsByTagName('bndbox')[0]
    w = root.getElementsByTagName('width')[0]
    h = root.getElementsByTagName('height')[0]

    xmin = bndbox.getElementsByTagName('xmin')[0]
    ymin = bndbox.getElementsByTagName('ymin')[0]
    xmax = bndbox.getElementsByTagName('xmax')[0]
    ymax = bndbox.getElementsByTagName('ymax')[0]

    xmin_data = xmin.childNodes[0].data
    ymin_data = ymin.childNodes[0].data
    xmax_data = xmax.childNodes[0].data
    ymax_data = ymax.childNodes[0].data
    w = int(w.childNodes[0].data)
    h = int(h.childNodes[0].data)

    xmin_parse = int(xmin_data) / w
    ymin_parse = int(ymin_data) / h
    xmax_parse = int(xmax_data) / w
    ymax_parse = int(ymax_data) / h

    box = np.array([[ymin_parse, xmin_parse, ymax_parse, xmax_parse]])

    return box


def tensor_to_xml(tensor, w, h):
    """
    tensor: Tensor (ymin, xmin, ymax, xmax)
    w : escala del eje x
    h : escala del eje y
    """
    ymin = int(tensor[0] * h)
    xmin = int(tensor[1] * w)
    ymax = int(tensor[2] * h)
    xmax = int(tensor[3] * w)

    return {'ymin': ymin, 'xmin': xmin, 'ymax': ymax, 'xmax': xmax}


class KernelRna():

    def __init__(self, containerName, configRna):
        self.containerName = containerName
        self.configRna = configRna
        self.status = 0
        self.detection_model = None

    def getStatus(self):
        return self.status

    def entrenar(self, catalogo, logger, singleton):

        logger.info("--------------   Entrenando Red   --------------")
        self.status = 1

        inicio = time.time()
        username = self.containerName
        logger.info("Username: {}".format(username))

        # El nombre del objeto a detectar, ejemplo 'taza'
        name_obj = self.configRna
        logger.info("Name Object Detect: {}".format(name_obj))

        logger.info("Load Images")
        lista_imagenes = catalogo.getObjeto(name_obj).getFotos()

        train_images_np = []
        for image_path in lista_imagenes:
            logger.info("==> Imagen: {}".format(image_path))

            ############### ALBI: # Me traigo cada imagen al temporal
            image_path = singleton.obtenerArchivo(image_path)
            img_numpy = load_image_into_numpy_array(image_path)
            train_images_np.append(img_numpy)

        logger.info("Load Anotation")
        lista_xml = catalogo.getObjeto(name_obj).getXml()

        logger.info("Anotation Xml to Numpy")
        gt_boxes = []
        for x_path in lista_xml:
            ############### ALBI: # Me traigo cada xml al temporal
            x_path = singleton.obtenerArchivo(x_path)
            x_numpy = xml_to_box_numpy_array(x_path)
            logger.info("==> Anotation: {} to Numpy: {}".format(x_path, x_numpy))
            gt_boxes.append(x_numpy)

        # -------------------------------------------------------------------

        # Load boxes in img train
        num_classes = 1
        label_id_offset = 1
        train_image_tensors = []
        gt_classes_one_hot_tensors = []
        gt_box_tensors = []
        for (train_image_np, gt_box_np) in zip(train_images_np, gt_boxes):
            train_image_tensors.append(tf.expand_dims(tf.convert_to_tensor(
                train_image_np, dtype=tf.float32), axis=0))
            gt_box_tensors.append(tf.convert_to_tensor(gt_box_np, dtype=tf.float32))
            zero_indexed_groundtruth_classes = tf.convert_to_tensor(
                np.ones(shape=[gt_box_np.shape[0]], dtype=np.int32) - label_id_offset)
            gt_classes_one_hot_tensors.append(tf.one_hot(zero_indexed_groundtruth_classes, num_classes))

        fin = time.time()
        logger.info("Done prepping data: Time {} segundos".format(str(fin - inicio)[0:7]))

        # -------------------------------------------------------------------

        inicio = time.time()
        # Load Model
        tf.keras.backend.clear_session()
        logger.info("Building model and restoring weights for fine-tuning...")

        # Hiperparametros
        num_classes = 1
        max_detections_per_class = 3
        max_total_detections = 3
        # ======================================

        pipeline_config = 'ssd_resnet50_v1_fpn_640x640_coco17_tpu-8/pipeline.config'
        checkpoint_path = 'ssd_resnet50_v1_fpn_640x640_coco17_tpu-8/checkpoint/ckpt-0'
        high, width = 640, 640  # Porque usamos la red ssd de la dimension 640x640

        # Load pipeline config and build a detection model.
        # ======================================
        # Since we are working off of a COCO architecture which predicts 90
        # class slots by default, we override the `num_classes` field here to be just
        # one (for our new rubber ducky class).
        configs = config_util.get_configs_from_pipeline_file(pipeline_config)
        model_config = configs['model']
        model_config.ssd.num_classes = num_classes
        model_config.ssd.post_processing.batch_non_max_suppression.max_detections_per_class = max_detections_per_class
        model_config.ssd.post_processing.batch_non_max_suppression.max_total_detections = max_total_detections
        model_config.ssd.freeze_batchnorm = True
        detection_model = model_builder.build(model_config=model_config, is_training=True)

        fake_box_predictor = tf.compat.v2.train.Checkpoint(
            _base_tower_layers_for_heads=detection_model._box_predictor._base_tower_layers_for_heads,
            # _prediction_heads=detection_model._box_predictor._prediction_heads,
            #    (i.e., the classification head that we *will not* restore)
            _box_prediction_head=detection_model._box_predictor._box_prediction_head,
        )
        fake_model = tf.compat.v2.train.Checkpoint(
            _feature_extractor=detection_model._feature_extractor,
            _box_predictor=fake_box_predictor)
        ckpt = tf.compat.v2.train.Checkpoint(model=fake_model)
        ckpt.restore(checkpoint_path).expect_partial()

        # Run model through a dummy image so that variables are created
        image, shapes = detection_model.preprocess(tf.zeros([1, high, width, 3]))
        prediction_dict = detection_model.predict(image, shapes)
        _ = detection_model.postprocess(prediction_dict, shapes)

        fin = time.time()
        logger.info("Weights restored! : Time {} segundos".format(str(fin - inicio)[0:7]))

        # tf.keras.backend.set_learning_phase(True)
        inicio = time.time()
        # These parameters can be tuned; since our training set has 5 images
        batch_size = 4
        learning_rate = 0.01
        num_batches = 500
        loss_min = 0.01

        # Select variables in top layers to fine-tune.
        trainable_variables = detection_model.trainable_variables
        to_fine_tune = []
        prefixes_to_train = [
            'WeightSharedConvolutionalBoxPredictor/WeightSharedConvolutionalBoxHead',
            'WeightSharedConvolutionalBoxPredictor/WeightSharedConvolutionalClassHead']
        for var in trainable_variables:
            if any([var.name.startswith(prefix) for prefix in prefixes_to_train]):
                to_fine_tune.append(var)

        # Set up forward + backward pass for a single train step.
        def get_model_train_step_function(model, optimizer, vars_to_fine_tune):
            """Get a tf.function for training step."""

            # Use tf.function for a bit of speed.
            # Comment out the tf.function decorator if you want the inside of the
            # function to run eagerly.
            @tf.function
            def train_step_fn(image_tensors,
                              groundtruth_boxes_list,
                              groundtruth_classes_list):
                """A single training iteration.

                Args:
                image_tensors: A list of [1, height, width, 3] Tensor of type tf.float32.
                    Note that the height and width can vary across images, as they are
                    reshaped within this function to be 640x640.
                groundtruth_boxes_list: A list of Tensors of shape [N_i, 4] with type
                    tf.float32 representing groundtruth boxes for each image in the batch.
                groundtruth_classes_list: A list of Tensors of shape [N_i, num_classes]
                    with type tf.float32 representing groundtruth boxes for each image in
                    the batch.

                Returns:
                A scalar tensor representing the total loss for the input batch.
                """
                shapes = tf.constant(batch_size * [[high, width, 3]], dtype=tf.int32)
                model.provide_groundtruth(
                    groundtruth_boxes_list=groundtruth_boxes_list,
                    groundtruth_classes_list=groundtruth_classes_list)
                with tf.GradientTape() as tape:
                    preprocessed_images = tf.concat(
                        [detection_model.preprocess(image_tensor)[0]
                         for image_tensor in image_tensors], axis=0)
                    prediction_dict = model.predict(preprocessed_images, shapes)
                    losses_dict = model.loss(prediction_dict, shapes)
                    total_loss = losses_dict['Loss/localization_loss'] + losses_dict['Loss/classification_loss']
                    gradients = tape.gradient(total_loss, vars_to_fine_tune)
                    optimizer.apply_gradients(zip(gradients, vars_to_fine_tune))
                return total_loss

            return train_step_fn

        optimizer = tf.keras.optimizers.SGD(learning_rate=learning_rate, momentum=0.9)
        train_step_fn = get_model_train_step_function(
            detection_model, optimizer, to_fine_tune)

        logger.info("Start fine-tuning!")
        for idx in range(num_batches):
            # Grab keys for a random subset of examples
            all_keys = list(range(len(train_images_np)))
            random.shuffle(all_keys)
            example_keys = all_keys[:batch_size]

            # Note that we do not do data augmentation in this demo.  If you want a
            # a fun exercise, we recommend experimenting with random horizontal flipping
            # and random cropping :)
            gt_boxes_list = [gt_box_tensors[key] for key in example_keys]
            gt_classes_list = [gt_classes_one_hot_tensors[key] for key in example_keys]
            image_tensors = [train_image_tensors[key] for key in example_keys]

            # Training step (forward pass + backwards pass)
            total_loss = train_step_fn(image_tensors, gt_boxes_list, gt_classes_list)

            if idx % 10 == 0:
                msj = 'batch ' + str(idx) + ' of ' + str(num_batches) + ', loss=' + str(total_loss.numpy())
                logger.info(msj)
                if idx >= 100 and (total_loss.numpy() < loss_min):
                    logger.info('Perdida aceptable => Detener entrenamiento')
                    break

        fin = time.time()
        logger.info("Done fine-tuning! : Time {} segundos".format(str(fin - inicio)[0:7]))

        # ===================================================
        inicio = time.time()
        logger.info("Start save model!")

        # Las dimensiones de las fotos originales, se guardara el metodo 'detection' con la firma del input.
        # Que son las dimensiones a hacer su proceso de validacion
        # dim_h, dim_w = 1024,1024  --> Probare con NONE y comparare los resultados

        @tf.function(input_signature=[tf.TensorSpec(shape=[None, None, None, 3], dtype=tf.float32)])
        def detect(input_tensor):
            """Run detection on an input image.

            Args:
                input_tensor: A [1, height, width, 3] Tensor of type tf.float32.
                Note that height and width can be anything since the image will be
                immediately resized according to the needs of the model within this
                function.

            Returns:
                A dict containing 3 Tensors (`detection_boxes`, `detection_classes`,
                and `detection_scores`).
            """
            preprocessed_image, shapes = detection_model.preprocess(input_tensor)
            prediction_dict = detection_model.predict(preprocessed_image, shapes)
            return detection_model.postprocess(prediction_dict, shapes)

        # Carpeta temporal que no persistiria
        export_dir = os.path.join('temp', username, name_obj, 'weigth')
        logger.info("Export Directory: {}".format(export_dir))

        try:
            os.mkdir(export_dir)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        tf.saved_model.save(
            detection_model, export_dir,
            signatures={
                'detect': detect.get_concrete_function()
            })

        fin = time.time()
        ############### ALBI: guardarArchivo
        singleton.guardarDirectorio(export_dir)
        logger.info("Save Model! : Time {} segundos".format(str(fin - inicio)[0:7]))

        self.status = 0

    def cargarWeigth(self, path_peso, logger, singleton):

        inicio = time.time()
        logger.info("-------------- Building model...")

        ############### ALBI: Nos traemos el folder del peso
        path_peso = singleton.obtenerDirectorio(path_peso)
        detection_model = tf.saved_model.load(path_peso)
        self.detection_model = detection_model
        fin = time.time()

        logger.info("Model restaured! : Time {} segundos".format(str(fin - inicio)[0:7]))

    def buscarObjeto(self, recinto, logger, singleton):
        """Objet Detection

        Args:
            recinto: path to img a detectar.
            logger: genera un archivo con los logs
            singleton: objeto que sirve como adapter con la persistencia
        """

        logger.info("--------------   Buscando Objeto   --------------")

        name_obj = self.configRna
        username = self.containerName
        path_peso = os.path.join(username, name_obj, 'weigth')

        logger.info("Name Object Detect: {}".format(name_obj))
        logger.info("Username: {}".format(username))
        logger.info("Path peso: {}".format(path_peso))

        if self.detection_model == None:
            self.cargarWeigth(path_peso, logger, singleton)
        else:
            logger.info('Weigth {} cargado'.format(path_peso))

        logger.info('Validation imagen...')
        ############### ALBI: Nos traemos la imagen a validar al temporal
        recinto = singleton.obtenerArchivo(recinto)
        im = Image.open(recinto)
        w, h = im.size
        logger.info("Width: {}".format(w))
        logger.info("Height: {}".format(h))
        img_filename = os.path.basename(recinto)

        test_images_np = []
        test_images_np.append(np.expand_dims(
            load_image_into_numpy_array(recinto), axis=0))

        input_tensor = tf.convert_to_tensor(test_images_np[0], dtype=tf.float32)
        detections = self.detection_model.signatures['detect'](input_tensor)

        logger.info("Name imagen to detect: {}".format(img_filename))
        score = detections['detection_scores'][0][0].numpy() * 100
        logger.info("Score detection: {:.2f}%".format(score))

        box = detections['detection_boxes'][0][0].numpy()
        logger.info("Detection Boxes: {}".format(box))

        box_resize = tensor_to_xml(box, w, h)
        logger.info("Box PascalVOC: {}".format(box_resize))

        criterio = score >= 70

        # BORRAR en produccion, en solo para ver el resultado en desarrollo
        # ===================================================
        dir_ruta = os.path.join(username, name_obj, 'result')
        try:
            os.mkdir(dir_ruta)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        ruta = os.path.join(dir_ruta, img_filename)
        logger.info("[INFO] Path Export: {}".format(ruta))

        label_id_offset = 1
        category_index = {1: {'id': 1, 'name': name_obj}}

        plot_detections(
            test_images_np[0][0],
            detections['detection_boxes'][0][:1].numpy(),
            detections['detection_classes'][0][:1].numpy().astype(np.uint32)
            + label_id_offset,
            detections['detection_scores'][0][:1].numpy(),
            category_index, figsize=(15, 20), image_name=ruta)

        # ===================================================

        return {'encontrado': criterio,
                'ubicaciones': box_resize,
                'precision': score}
