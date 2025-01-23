from paddleocr import PaddleOCR
import os
import sys

def main(input_dir, output_dir):
    ocr = PaddleOCR(use_angle_cls=True, lang='japan')
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        file_path = os.path.join(input_dir, filename)
        if not os.path.isfile(file_path):
            continue

        result = ocr.ocr(file_path, det=True, rec=True)
        output_file = os.path.join(output_dir, f"{filename}.txt")
        with open(output_file, "w") as f:
            for line in result[0]:
                f.write(f"{line[1][0]}\n")

if __name__ == "__main__":
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    main(input_dir, output_dir)

