import cv2
import mediapipe as mp
import time


class FaceDetector():
    def __init__(self, minDetectionCon=0.5):
        self.minDetectionCon = minDetectionCon

        self.mpFaceDetection = mp.solutions.face_detection
        self.mpDraw = mp.solutions.drawing_utils
        self.faceDetection = self.mpFaceDetection.FaceDetection(self.minDetectionCon)

    def findFaces(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.faceDetection.process(imgRGB)
        # print(self.results.detections)

        bboxs = []

        if self.results.detections:
            for id, detection in enumerate(self.results.detections):
                # mpDraw.draw_detection(img,detection)
                # print(id,detection)
                # print(detection.score)
                # print(detection.location_data.relative_bounding_box)
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, ic = img.shape
                bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
                    int(bboxC.width * iw), int(bboxC.height * ih)

                bboxs.append([id, bbox, detection.score])

                cv2.rectangle(img, bbox, (255, 0, 255), 2)
                # print(int(detection.score[0] * 100))
                cv2.putText(img, f'FPS: {int(detection.score[0] * 100)}%', (bbox[0], bbox[1] - 20),
                            cv2.FONT_HERSHEY_PLAIN,
                            3, (255, 0, 0), 2)

                return img, bboxs


def main():
    cap = cv2.VideoCapture("C:\\Users\\Sithira Bimsara\\Downloads\\Stock Videos\\face1.mp4")
    pTime = 0
    detector = FaceDetector()

    while True:
        success, img = cap.read()
        if not success:
            break

        detection_results = detector.findFaces(img)
        if detection_results is not None:
            img, bboxs = detection_results
        else:
            bboxs = []

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 2)
        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
