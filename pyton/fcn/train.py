import tensorflow as tf
from model import FCN_model
from generator import Generator
import os
import sys

def train(model, train_generator, val_generator, epochs=50, checkpoint_path='./snapshots'):
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
                    loss='categorical_crossentropy',
                    metrics=['accuracy'])

    os.makedirs(checkpoint_path, exist_ok=True)
    model_path = os.path.join(checkpoint_path, 'model_epoch_{epoch:02d}_loss_{loss:.2f}_acc_{accuracy:.2f}_val_loss_{val_loss:.2f}_val_acc_{val_accuracy:.2f}.h5')
    
    history = model.fit(train_generator,
                        steps_per_epoch=len(train_generator),
                        epochs=epochs,
                        callbacks=[tf.keras.callbacks.ModelCheckpoint(model_path, monitor='val_loss', save_best_only=True, verbose=1)],
                        validation_data=val_generator,
                        validation_steps=len(val_generator))

    return history

if __name__ == "__main__":
    print('cmd entry:', sys.argv)
    BASE_PATH = os.getcwd()
    if len( sys.argv ) > 1 :
          BASE_PATH = sys.argv[1]
    # Create FCN model
    model = FCN_model(len_classes=5, dropout_rate=0.2)
    # The below folders are created using utils.py
    train_dir = BASE_PATH+'/processedDataSetAds/train'
    val_dir = BASE_PATH+'/processedDataSetAds/val'
    checkpoint_path = BASE_PATH + "/snapshotsTest"
    
    # If you get out of memory error try reducing the batch size
    BATCH_SIZE=8
    if len( sys.argv ) > 2 :
          BATCH_SIZE = int(sys.argv[2])
    train_generator = Generator(train_dir, BATCH_SIZE, shuffle_images=True, image_min_side=24)
    val_generator = Generator(val_dir, BATCH_SIZE, shuffle_images=True, image_min_side=24)

    EPOCHS=50
    if len( sys.argv ) > 3 :
          EPOCHS = int(sys.argv[3])
    history = train(model, train_generator, val_generator, epochs=EPOCHS, checkpoint_path =checkpoint_path)
