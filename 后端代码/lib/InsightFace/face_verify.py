import cv2
from PIL import Image
import argparse
from pathlib import Path
# from multiprocessing import Process, Pipe,Value,Array
import torch
from lib.InsightFace.config import get_config
from lib.InsightFace.mtcnn import MTCNN
from lib.InsightFace.Learner import face_learner
from lib.InsightFace.utils import load_facebank, draw_box_name, prepare_facebank


def recognize(frame, mtcnn, targets, names, learner, conf):
    """
    从捕获到的图片中识别facedata中存在的人脸，并返回标定好的图片
    :param frame:
    :return:
    """
    image = Image.fromarray(frame)
    # 提取ROI, 脸部特征点坐标
    bboxes, faces = mtcnn.align_multi(image, conf.face_limit, conf.min_face_size)
    bboxes = bboxes[:, :-1]  # shape:[10,4],only keep 10 highest possibiity faces
    bboxes = bboxes.astype(int)
    bboxes = bboxes + [-1, -1, 1, 1]  # personal choice
    results, score = learner.infer(conf, faces, targets, tta=False)
    all_names = []
    for idx, bbox in enumerate(bboxes):
        # if args.score:
        #     res_frame = draw_box_name(bbox, names[results[idx] + 1] + '_{:.2f}'.format(score[idx]), frame)
        # else:
        res_frame = draw_box_name(bbox, names[results[idx] + 1], frame)
        all_names.append(names[results[idx] + 1])
    return res_frame, all_names


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='for face verification')
    parser.add_argument("-s", "--save", help="whether save",action="store_true")
    parser.add_argument('-th','--threshold',help='threshold to decide identical faces',default=1.54, type=float)
    parser.add_argument("-u", "--update", help="whether perform update the facebank",action="store_true")
    parser.add_argument("-tta", "--tta", help="whether test time augmentation",action="store_true")
    parser.add_argument("-c", "--score", help="whether show the confidence score",action="store_true")
    args = parser.parse_args()

    conf = get_config(False)

    mtcnn = MTCNN()
    print('mtcnn loaded')

    learner = face_learner(conf, True)
    learner.threshold = args.threshold
    if conf.device.type == 'cpu':
        learner.load_state(conf, 'cpu_final.pth', True, True)
    else:
        learner.load_state(conf, 'final.pth', True, True)
    learner.model.eval()
    print('learner loaded')
    
    if args.update:
        targets, names = prepare_facebank(conf, learner.model, mtcnn, tta=args.tta)
        print('facebank updated')
    else:
        targets, names = load_facebank(conf)
        print('facebank loaded')

    # inital camera
    cap = cv2.VideoCapture(0)
    cap.set(3,1280)
    cap.set(4,720)
    if args.save:
        video_writer = cv2.VideoWriter(conf.data_path/'recording.avi', cv2.VideoWriter_fourcc(*'XVID'), 6, (1280,720))
        # frame rate 6 due to my laptop is quite slow...
    while cap.isOpened():
        isSuccess, frame = cap.read()
        if isSuccess:            
            try:
                frame, _ = recognize(frame, mtcnn, targets, names, learner, conf)
            except:
                print('detect error')    

            cv2.imshow('face Capture', frame)

        if args.save:
            video_writer.write(frame)

        if cv2.waitKey(1)&0xFF == ord('q'):
            break

    cap.release()
    if args.save:
        video_writer.release()
    cv2.destroyAllWindows()
