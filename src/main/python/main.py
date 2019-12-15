import os, sys
sys.path.append("..")
import glob
import imageio
import tensorflow as tf
import keras, keras.layers as L, keras.backend as K
import numpy as np
from scipy.misc import imresize
import numpy as np
import pickle

#Constants
IMG_SHAPE = (224, 224, 3)
CODE_SIZE = 64

#Get right application directory
if getattr(sys, 'frozen', False):
    # If the application is run as a bundle, the pyInstaller bootloader
    # extends the sys module by a flag frozen=True and sets the app 
    # path into variable _MEIPASS'.
    application_path = sys._MEIPASS
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

#Get a list of paths to all images in a given directory and subdirectories
def get_image_paths(path=".", extensions=["jpg","jpeg","png","tga","bmp"]):
    result = []
    _ = [result.extend(glob.glob(os.path.join(path, '**/*.%s' % ext), recursive=True)) for ext in extensions]
    return result

#Load images in resized form (Currently unused, takes long and way too much RAM)
def load_images(paths):
    images = []
    for path in paths:
        images.append(imresize(imageio.imread(path, pilmode="RGB"), IMG_SHAPE, interp="bilinear"))
    return np.concatenate([aux[None,...] for aux in images], axis=0)

#Reset TF session every time a new NN is built
def reset_tf_session():
    curr_session = tf.get_default_session()
    # close current session
    if curr_session is not None:
        curr_session.close()
    # reset graph
    K.clear_session()
    # create new session
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    s = tf.InteractiveSession(config=config)
    K.set_session(s)
    return s

#Neural Networks
def build_pca_autoencoder(img_shape = IMG_SHAPE, code_size = CODE_SIZE, weight_file = os.path.join(application_path, "encoder_pca.h5")):
    """
    Here we define a simple linear autoencoder.
    We also flatten and un-flatten data to be compatible with image shapes
    """
    
    encoder = keras.models.Sequential()
    encoder.add(L.InputLayer(img_shape))
    encoder.add(L.Flatten())                  #flatten image to vector
    encoder.add(L.Dense(code_size))           #actual encoder
    
    encoder.load_weights(weight_file)
    
    return encoder

def build_deep_autoencoder(img_shape = IMG_SHAPE, code_size = CODE_SIZE, weight_file = os.path.join(application_path, "encoder.h5")):
    """PCA's deeper brother."""
    
    encoder = keras.models.Sequential()
    encoder.add(L.InputLayer(img_shape))
    encoder.add(L.Conv2D(filters=32, kernel_size=(3,3), padding="same", activation="elu"))
    encoder.add(L.MaxPooling2D(pool_size=(2,2)))
    encoder.add(L.Conv2D(filters=64, kernel_size=(3,3), padding="same", activation="elu"))
    encoder.add(L.MaxPooling2D(pool_size=(2,2)))
    encoder.add(L.Conv2D(filters=128, kernel_size=(3,3), padding="same", activation="elu"))
    encoder.add(L.MaxPooling2D(pool_size=(2,2)))
    encoder.add(L.Conv2D(filters=256, kernel_size=(3,3), padding="same", activation="elu"))
    encoder.add(L.MaxPooling2D(pool_size=(2,2)))
    encoder.add(L.Flatten())
    encoder.add(L.Dense(code_size))
    
    encoder.load_weights(weight_file)
    
    return encoder

#Load weights later
def load_NN_weights(encoder, path):
    encoder.load_weights(path)

# Build code database, returns a dictionary of dictionaries containing image paths and the respective codes
def build_code_database(encoder, paths, callback, graph):
    codes = {}
    i = 0
    with graph.as_default():
        for p in paths:
            codes[i]={'path':p, 'name':os.path.basename(p), 'code':encoder.predict(imresize(imageio.imread(p, pilmode="RGB"), IMG_SHAPE, interp="bilinear")[None])}
            i += 1
            callback(i, len(paths))
        return codes

def save_database(database, name, overwrite=False):
    if((os.path.isfile(name) and overwrite) or not os.path.isfile(name)):
        pickle.dump(database, open(name, "wb"))
    elif(os.path.isfile(name) and not overwrite):
        i = 1
        n, ext = os.path.split(name)
        while(os.path.isfile(n + i + ext)):
            i += 1
        pickle.dump(database, open(n + i + ext, "wb"))

def load_database(name):
    if(os.path.isfile(name)):
        return pickle.load(open(name, "rb"))

# Compare input image to database (using euclidean distance aka L2 norm of the codes)
def l2_norm(v, u):
    return np.linalg.norm(v - u)

def similarity_search(inp_path, database, encoder, max_dist=0):
    code = encoder.predict(imresize(imageio.imread(inp_path, pilmode="RGB"), IMG_SHAPE, interp="bilinear")[None])
    hits = []
    for d in database.values():
        dist = l2_norm(code, d['code'])
        if max_dist == -1 or dist <= max_dist:
            d['distance'] = dist
            hits.append(d)
    return hits
    
###############################################################################
# PyQt5 app
###############################################################################

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from fbs_runtime.application_context.PyQt5 import ApplicationContext

from tablemodel import TableModel

class Build_Thread(QThread):
    """
    Runs the database building thread
    """
    processed = pyqtSignal(int, int)
    finished = pyqtSignal(dict)
    close = pyqtSignal()
    
    def __init__(self, encoder, paths, graph, parent=None):
        super(Build_Thread, self).__init__(parent)
        self.encoder = encoder
        self.paths = paths
        self.graph = graph
    
    def run(self):
        database = build_code_database(self.encoder, self.paths, self.processed.emit, self.graph)
        self.finished.emit(database)
        self.close.emit()

class ImageSimilarity(QWidget):
    """
    Main class
    """
    def __init__(self, parent=None):
        super(ImageSimilarity, self).__init__(parent)
        
        #Build window
        self.setWindowTitle('Image Similarity Search')
        self.radio_pca = QRadioButton('PCA')
        self.radio_pca.setChecked(True)
        self.radio_deep = QRadioButton('Convolutional')
        self.button_load_weights = QPushButton('Load Weights')
        self.button_build_DB = QPushButton('Build Database')
        self.button_save_DB = QPushButton('Save Database')
        self.button_load_DB = QPushButton('Load Database')
        self.button_load_img = QPushButton('Load Image')
        self.button_search = QPushButton('Search')
        self.button_search.setEnabled(False)
        self.button_save_result = QPushButton('Save Result')
        self.button_save_result.setEnabled(False)
        self.spinbox = QSpinBox()
        self.spinbox.setMinimum(-1)
        self.spinbox.setMaximum(99999)
        self.spinbox.setValue(0)
        self.spinboxlabel = QLabel('Max. Distance:')
        self.spinboxlabel.setAlignment(Qt.AlignRight)
        self.searchlabel = QLabel('Query Image:')
        self.countlabel = QLabel('# of Hits:')
        self.table = QTableView()
        #self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.model = TableModel(parent=self)
        self.table.setModel(self.model)
        self.table.setSortingEnabled(True)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        hbox_radio = QHBoxLayout()
        hbox_radio.addWidget(self.radio_pca)
        hbox_radio.addWidget(self.radio_deep)
        hbox_radio.addWidget(self.button_load_weights)
        
        hbox_buttons = QHBoxLayout()
        hbox_buttons.addWidget(self.button_build_DB)
        hbox_buttons.addWidget(self.button_load_DB)
        hbox_buttons.addWidget(self.button_save_DB)
        hbox_buttons.addWidget(self.button_load_img)
        hbox_buttons.addWidget(self.button_search)
        hbox_buttons.addWidget(self.spinboxlabel)
        hbox_buttons.addWidget(self.spinbox)
        
        radio_widget = QWidget()
        radio_widget.setLayout(hbox_radio)
        
        button_widget = QWidget()
        button_widget.setLayout(hbox_buttons)
        
        external_layout = QVBoxLayout()
        external_layout.addWidget(radio_widget)
        external_layout.addWidget(button_widget)
        external_layout.addWidget(self.searchlabel)
        external_layout.addWidget(self.countlabel)
        external_layout.addWidget(self.table)
        external_layout.addWidget(self.button_save_result)
        
        self.setLayout(external_layout)
        
        #Connect signals and slots
        self.radio_pca.toggled.connect(lambda:self.switch_NN(self.radio_pca))
        self.radio_deep.toggled.connect(lambda:self.switch_NN(self.radio_deep))
        self.button_load_weights.clicked.connect(self.load_weights)
        self.button_build_DB.clicked.connect(self.build_DB)
        self.button_load_DB.clicked.connect(self.load_DB)
        self.button_save_DB.clicked.connect(self.save_DB)
        self.button_load_img.clicked.connect(self.load_image)
        self.button_search.clicked.connect(self.search)
        self.button_save_result.clicked.connect(self.save_search)
        
        #Build neural network
        self.encoder = build_pca_autoencoder()
        
        #See if a database already exists
        if not os.path.isfile(os.path.join(application_path, 'std_db_pca.p')):
            self.firstTimeStart(os.path.join(application_path, 'std_db_pca.p'))
        else:
            self.database = load_database(os.path.join(application_path, 'std_db_pca.p'))

    def firstTimeStart(self, savename):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Please select a directory to search for images in. This will then build the search database.")
        msg.setWindowTitle("Setup")
        msg.setStandardButtons(QMessageBox.Ok)
        if msg.exec_():
            dir = None
            while not dir:
                dir = QFileDialog.getExistingDirectory(self, 'Choose Search Root', QDir.homePath(), QFileDialog.ShowDirsOnly)
            paths = get_image_paths(dir)
            self.progresswindow = self.make_progress_window(len(paths))
            self.progresswindow.show()
            graph = tf.get_default_graph()
            build_thread = Build_Thread(self.encoder, paths, graph, self)
            build_thread.processed.connect(self.update_progress)
            build_thread.finished.connect(self.set_database)
            build_thread.finished.connect(lambda db: save_database(db, savename))
            build_thread.close.connect(self.progresswindow.close)
            build_thread.close.connect(lambda : self.build_message(savename))
            build_thread.start()
    
    def build_message(self, savename=None):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Database complete!")
        if not savename:
            msg.setInformativeText("Don't forget to save your database to avoid having to rebuild it upon program restart.")
        else:
            msg.setInformativeText("The database was saved as {} and will be loaded as default on all subsequent program starts.".format(savename))
        msg.setWindowTitle("Completed")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
    
    def make_progress_window(self, max):
        window = QDialog(self)
        window.setWindowTitle("Building Search Database")
        self.progress = QProgressBar(window)
        self.progress.setMaximum(max)
        self.progresslabel = QLabel(window)
        self.progresslabel.setText("Processed: 0 of {}".format(max))
        layout = QVBoxLayout()
        window.setLayout(layout)
        layout.addWidget(self.progresslabel)
        layout.addWidget(self.progress)
        window.setModal(Qt.ApplicationModal)
        return window
    
    def update_progress(self, prog, max):
        self.progresslabel.setText("Processed: {} of {}".format(prog, max))
        self.progress.setValue(prog)
    
    def set_database(self, db):
        self.database = db
    
    def load_image(self):
        f, _ = QFileDialog.getOpenFileName(self, 'Load Image', QDir.homePath(), "Image Files (*.jpg *.jpeg *.png *.tga *.bmp)")
        if f:
            self.search_img_path = f
            self.searchlabel.setText('Query Image: {}'.format(os.path.basename(f)))
            if not self.button_search.isEnabled():
                self.button_search.setEnabled(True)
    
    def search(self):
        if self.search_img_path:
            self.lastSearchQuery = self.search_img_path
            if not self.button_save_result.isEnabled():
                self.button_save_result.setEnabled(True)
            hits = similarity_search(self.search_img_path, self.database, self.encoder, self.spinbox.value())
            self.countlabel.setText('# of hits: {}'.format(str(len(hits))))
            #Update Table Model
            self.model.removeRows(0, self.model.rowCount())
            for hit in hits:
                row = {"name":hit['name'], "path":hit['path'], "distance":hit['distance']}
                self.model.appendRow(row)
    
    def save_search(self):
        filename, _ = QFileDialog.getSaveFileName(self, 'Save Result', QDir.currentPath(), 'Text files (*.txt)')
        if filename:
            with open(filename, "w") as file:
                file.write("Query image: {}\n\n".format(self.lastSearchQuery))
                for i in range(self.model.rowCount()):
                    file.write("Name: {}, Path: {}, Distance: {}\n".format(self.model.results[i]['name'], self.model.results[i]['path'], self.model.results[i]['distance']))

    def switch_NN(self, b):
        if b.text() == 'PCA' and b.isChecked():
            reset_tf_session()
            self.encoder = build_pca_autoencoder()
            self.database = load_database(os.path.join(application_path, 'std_db_pca.p'))
            self.search_img_path = None
            self.button_search.setEnabled(False)
        elif b.text() == 'Convolutional' and b.isChecked():
            reset_tf_session()
            self.encoder = build_deep_autoencoder()
            if os.path.isfile(os.path.join(application_path, 'std_db_deep.p')):
                self.database = load_database(os.path.join(application_path, 'std_db_deep.p'))
            else:
                self.firstTimeStart(os.path.join(application_path, 'std_db_deep.p'))
            self.search_img_path = None
            self.button_search.setEnabled(False)
        else:
            pass
    
    def load_weights(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Load Weights', QDir.currentPath(), 'Neural Network Weights (*.h5)')
        if filename:
            load_NN_weights(self.encoder, filename)
    
    def build_DB(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.Directory)
        if dlg.exec_():
            dirs = dlg.selectedFiles()
            paths = get_image_paths(dirs[0])
            self.progresswindow = self.make_progress_window(len(paths))
            self.progresswindow.show()
            graph = tf.get_default_graph()
            build_thread = Build_Thread(self.encoder, paths, graph, self)
            build_thread.processed.connect(self.update_progress)
            build_thread.finished.connect(self.set_database)
            build_thread.close.connect(self.progresswindow.close)
            build_thread.close.connect(self.build_message)
            build_thread.start()
    
    def load_DB(self):
        dbname, _ = QFileDialog.getOpenFileName(self, 'Load Database', QDir.currentPath(), "Database files (*.p)")
        if dbname:
            self.database = load_database(dbname)
    
    def save_DB(self):
        filename, _ = QFileDialog.getSaveFileName(self, 'Save Database', QDir.currentPath(), 'Database files (*.p)')
        if filename:
            save_database(self.database, filename, True)

def main():
    appctxt = ApplicationContext()       # 1. Instantiate ApplicationContext
    ex = ImageSimilarity()
    ex.show()
    exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)

if __name__ == '__main__':
    main()