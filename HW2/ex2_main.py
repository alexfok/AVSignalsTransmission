import sys
import numpy as np
import matplotlib.pyplot as plt
import cv2
import os

def read_yuv_file(filename, width, height, frame_index):
    # Read the YUV data for a particular frame into a numpy array
    # print('read_yuv_file1 frame height: {}, width: {}'.format(height, width))
    num_pixels = width * height
    with open(filename, "rb") as fp:
        fp.seek(num_pixels * 3 // 2 * frame_index)
        buffer = np.fromfile(fp, dtype=np.uint8, count=num_pixels * 3 // 2)

    # Extract the Y channel and reshape into a 2D array
    y_plane = buffer[:num_pixels].reshape((height, width))
    height1, width1 = y_plane.shape
#    print('read_yuv_file2 frame height: {}, width: {}, height1: {}, width1: {}'.format(height, width, height1, width1))

    return y_plane

def calculate_sad(frame1, frame2):
    # Calculate the sum of absolute differences (SAD) between two blocks
    return np.sum(np.abs(frame1 - frame2))

def calculate_mad(frame1, frame2):
    diff = np.abs(frame1.astype(np.float32) - frame2.astype(np.float32))
    return np.mean(diff)

def psnr(frame_index1, frame_index2):
    frame1 = read_yuv_file(filename, width, height, frame_index1)
    frame2 = read_yuv_file(filename, width, height, frame_index2)
    # Calculate MSE
    mse = np.mean((frame1 - frame2) ** 2)

    # Calculate PSNR
    max_pixel = 255.0
    psnr = 10 * np.log10((max_pixel ** 2) / mse)

    return psnr

def psnr_frames(frame1, frame2):
    # Calculate MSE
    mse = np.mean((frame1 - frame2) ** 2)

    # Calculate PSNR
    max_pixel = 255.0
    psnr = 10 * np.log10((max_pixel ** 2) / mse)

    return psnr

def display_frame(filename, width, height, frame_index):
    frame = read_yuv_file(filename, width, height, frame_index)
    cv2.imshow(f"Motion vectors for frame {frame_index}", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def frame_diff(frame1, frame2):
    # Calculate difference between frames
    diff = cv2.absdiff(frame1, frame2)

    return diff

def display_frames_diff3(filename, width, height, frame_index1, frame_index2):
    frame1 = read_yuv_file(filename, width, height, frame_index1)
    frame2 = read_yuv_file(filename, width, height, frame_index2)
    img = cv2.absdiff(frame1, frame2)

    cv2.imshow(f"Frames difference {frame_index2}", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return img

def display_frames_diff4(filename, width, height, frame_index1, frame2):
    frame1 = read_yuv_file(filename, width, height, frame_index1)
#    frame2 = read_yuv_file(filename, width, height, frame_index2)
    img = cv2.absdiff(frame1, frame2)

    cv2.imshow(f"Frames difference {frame_index2}", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    # Calculate PSNR
    # Calculate MSE
    mse = np.mean((frame1 - frame2) ** 2)

    # Calculate PSNR
    max_pixel = 255.0
    psnr = 10 * np.log10((max_pixel ** 2) / mse)
    print('psnr between frame_index1: {} and reconstructed frame {}'.format(frame_index1, psnr))
    return img

def save_frames(frame, filename, test_mode, qp, check_frame1, check_frame2, check_frame3):
    psnr = psnr_frames(frame, check_frame3)
    print(f'psnr: {psnr:.6f}')
    text = f'psnr: {psnr:.6f}'
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.6
    color = (255, 0, 0)  # White font in color grey scale image
    thickness = 2
    # Draw the text on the image
    cv2.putText(check_frame3, text, (20, 50), font, font_scale, color, thickness)

    mad = calculate_mad(frame, check_frame3)
    print(f'mad: {mad:.6f}')
    text = f'mad: {mad:.6f}'
    # Draw the text on the image
    cv2.putText(check_frame3, text, (20, 20), font, font_scale, color, thickness)
#    color = (0, 0, 0)  # White font in color grey scale image
#    cv2.putText(check_frame2, text, (20, 50), font, font_scale, color, thickness)

    img_file_name = os.path.splitext(os.path.basename(filename))[0]
    cv2.imwrite(f"images/{img_file_name}_predicted_frame_{test_mode}_{qp}.png",check_frame1)
    cv2.imwrite(f"images/{img_file_name}_residual_frame_{test_mode}_{qp}.png",check_frame2)
    cv2.imwrite(f"images/{img_file_name}_reconstructed_frame_{test_mode}_{qp}.png",check_frame3)
#        cv2.imshow(f"predicted_frame_{mode}", check_frame1)
#        cv2.imshow(f"residual_frame_{mode}", check_frame2)
#        cv2.imshow(f"reconstructed_frame_{mode}", check_frame3)
    #    cv2.imshow(f"check_frame1 {mode}", check_frame1)
#        cv2.waitKey(0)
#        cv2.destroyAllWindows()

def test_intra_pred_modes(filename, frame_index1, qp, block_size = 4, height = 288, width = 352):
    frame = read_yuv_file(filename, width, height, frame_index1)
    height, width = frame.shape[:2]
    num_blocks_h = height // block_size
    num_blocks_w = width // block_size

    check_frame1 = np.zeros_like(frame)
    check_frame2 = np.zeros_like(frame)
    check_frame3 = np.zeros_like(frame)
    predicted_frame = np.zeros_like(frame)
#    print('mode {}, height {}, width {}, num_blocks_h {}, num_blocks_w {}'.format(mode, height, width, num_blocks_h, num_blocks_w))

    # for all blocks
        # reconstruct source block == predicted block + residual block
        # keep residual block in residual frame
        # keep reconstructed block in reconstructed frame
    # return - reconstructed and residual frames
    for test_mode in range(modes_number):
        print(f'test_intra_pred_modes: test_mode {test_mode}')
        for blk_y in range(num_blocks_h):
            for blk_x in range(num_blocks_w):
                start_x = blk_x * block_size
                start_y = blk_y * block_size

                # Calculate all intra prediction modes
                # Calculate SAD
                # Mode with minimal SAD is chosen
                predicted_block, min_mode = calculate_intra_pred_modes(frame, start_x, start_y, block_size, test_mode)
                # Check Point
                check_frame1[start_y:start_y + block_size, start_x:start_x + block_size] = predicted_block
                # Predicted block is subtracted from source block to get residual block
                residual_block = frame[start_y:start_y + block_size, start_x:start_x + block_size] - predicted_block
                # Check Point
                check_frame2[start_y:start_y + block_size, start_x:start_x + block_size] = residual_block
                # residual block is transformed, quantized, inverse transformed and scaled to reconstruct source block
                residual_block_transformed = dct_transform_block_main(residual_block, qp = qp, block_size = block_size)
                reconstructed_block = predicted_block + residual_block_transformed
                # Check Point
                check_frame3[start_y:start_y + block_size, start_x:start_x + block_size] = reconstructed_block
        # Display the predicted frame for the current mode

        save_frames(frame, filename, test_mode, qp, check_frame1, check_frame2, check_frame3)

def get_predictor_r(frame, start_x, start_y, width, height, block_size):
    if start_y - 1 >= 0 and start_x < width:
        predictor = frame[start_y - 1, start_x]
    else:
        predictor = 128
    return predictor

def calculate_intra_pred_modes(frame, start_x, start_y, block_size, test_mode = -1):
    # Perform inter prediction for each mode
    # print(f'start_x {start_x}, start_y {start_y}')
    predicted_block_list = []
    predicted_block = None
    min_mod = -1
#    predicted_block = np.zeros((block_size,block_size))
    for mode in range(modes_number):
        # Perform inter prediction for each mode
        predicted_block_list.append(np.zeros((block_size,block_size)))
    for mode in range(modes_number):
            if mode == 0:  # Vertical (North)
                if start_y - 1 >= 0:
                    for idx in range(block_size):
                        start_xl = start_x + idx
                        if start_xl < width:
                            #aa = frame[start_y:start_yl, start_x - 1]
                            # aa = frame[start_y - 1, start_x + start_xl]
                            # print(start_y,start_xl, start_x)
                            # print(aa)
                            # print(f'if start_xl: {start_xl}')
                            # predicted_block[:, :start_xl] = 58
                            # print(f'predicted_block1: {predicted_block}')
                            predicted_block_list[mode][:, :start_xl] = frame[start_y - 1, start_xl]
                            # print(f'predicted_block2:\n {predicted_block}')
                            # print(f'frame[start_y - 1, start_xl]: {frame[start_y - 1, start_xl]}')
                        else:
                            # print(f'else start_xl: {start_xl}')
                            predicted_block_list[mode][:, :start_xl] = 128
                else:
                    # print(f'else start_y: {start_y}')
                    predicted_block_list[mode][:, :] = 128
            elif mode == 1:  # Horizontal (West)
#                predicted_frame[start_y:start_y + block_size, start_x:start_x + block_size] = frame[start_y:start_y + block_size, start_x - block_size:start_x]
                if start_x - 1 >= 0:
                    for idx in range(block_size):
                        start_yl = start_y + idx
                        if start_yl < height:
                            # aa = frame[start_y:start_yl, start_x - 1]
                            # print(aa)
                            predicted_block_list[mode][:start_yl, :] = frame[start_yl, start_x - 1]
                        else:
                            predicted_block_list[mode][:start_yl, :] = 128
                else:
                    predicted_block_list[mode][:, :] = 128
            elif mode == 2:  # DC (Average)
                # top = frame[start_y - block_size:start_y, start_x:start_x + block_size]
                # left = frame[start_y:start_y + block_size, start_x - block_size:start_x]
                top = frame[start_y:start_y +  block_size, start_x:start_x + block_size]
                left = frame[start_y:start_y + block_size, start_x:start_x + block_size]
                predicted_block_list[mode][:, :] = (np.mean(top) + np.mean(left)) / 2
            elif mode == 3:  # Diagonal Down Left (Northwest)
                    # Iterate over diagonals starting from the top-left corner
                    for k in range(block_size + block_size - 1):
                        predictor = get_predictor_r(frame, start_x, start_y, width, height, block_size)
                        for i in range(block_size):
                            for j in range(block_size):
                                if i + j == k:
                                    predicted_block_list[mode][i, j] = predictor

            elif mode == 4:  # Diagonal Down Right (Northeast)
                    # Iterate over diagonals starting from the top-right corner
                    for k in range(block_size + block_size - 1):
                        predictor = get_predictor_r(frame, start_x, start_y, width, height, block_size)
                        for i in range(block_size):
                            j = block_size - 1 - k + i
                            if j >= 0 and j < block_size:
                                predicted_block_list[mode][i, j] = predictor
            elif mode == 5:  # Vertical Right (North-Northeast)
                    for k in range(block_size + block_size - 1):
                        predictor = get_predictor_r(frame, start_x, start_y, width, height, block_size)
                        for i in range(block_size-1, -1, -1):
                            j = k - i
                            if j >= 0 and j < block_size:
                                predicted_block_list[mode][i, j] = predictor
            elif mode == 6:  # Horizontal Down (West-Northwest)
                    for k in range(block_size + block_size - 1):
                        predictor = get_predictor_r(frame, start_x, start_y, width, height, block_size)
                        for j in range(block_size-1, -1, -1):
                            i = k - j
                            if i >= 0 and i < block_size:
                                predicted_block_list[mode][i, j] = predictor
            elif mode == 7:  # Vertical Left (North-Northwest)
                    for k in range(block_size + block_size - 1):
                        predictor = get_predictor_r(frame, start_x, start_y, width, height, block_size)
                        for i in range(block_size):
                            j = i - k
                            if j >= 0 and j < block_size:
                                predicted_block_list[mode][i, j] = predictor
            elif mode == 8:  # Horizontal Up (West-Northeast)
                    for k in range(block_size + block_size - 1):
                        predictor = get_predictor_r(frame, start_x, start_y, width, height, block_size)
                        for j in range(block_size):
                            i = block_size - 1 - k + j
                            if i >= 0 and i < block_size:
                                predicted_block_list[mode][i, j] = predictor
    if test_mode == -1:
        min_sad = 1000000
        for mode in range(modes_number):
            # Perform inter prediction for each mode
            cur_predicted_block = predicted_block_list[mode]
            source_block = frame[start_y:start_y +  block_size, start_x:start_x + block_size]
            cur_sad = calculate_sad(source_block, cur_predicted_block)
    #        print(f'cur_sad: {cur_sad}, min_sad: {min_sad}')
            if cur_sad < min_sad:
                # print(f'mode: {mode}, cur_sad: {cur_sad}, min_sad: {min_sad}')
                predicted_block = cur_predicted_block
                min_sad = cur_sad
                min_mod = mode
    #    if start_y % 10 == 0:
    #        print(f'\n mode {mode}, predicted_block: \n {predicted_block} \n')
    #        print(f'mode: {mode}, min_sad: {min_sad}')
    else:
        predicted_block = predicted_block_list[test_mode]
    return predicted_block, min_mod

def inter_prediction_blocks_main(filename, frame_index1, qp, block_size = 4, height = 288, width = 352):

    frame = read_yuv_file(filename, width, height, frame_index1)
    height, width = frame.shape[:2]
    num_blocks_h = height // block_size
    num_blocks_w = width // block_size

    check_frame1 = np.zeros_like(frame)
    check_frame2 = np.zeros_like(frame)
    check_frame3 = np.zeros_like(frame)
    predicted_frame = np.zeros_like(frame)
    mode_freq_list = [0] * 8
    mode_pred_list = [0] * 8
    prev_mod = -1
#    print('mode {}, height {}, width {}, num_blocks_h {}, num_blocks_w {}'.format(mode, height, width, num_blocks_h, num_blocks_w))

    # for all blocks
        # reconstruct source block == predicted block + residual block
        # keep residual block in residual frame
        # keep reconstructed block in reconstructed frame
    # return - reconstructed and residual frames
    for blk_y in range(num_blocks_h):
        for blk_x in range(num_blocks_w):
            start_x = blk_x * block_size
            start_y = blk_y * block_size

            # Calculate all intra prediction modes
            # Calculate SAD
            # Mode with minimal SAD is chosen
            # mode = -1
            predicted_block, min_mod = calculate_intra_pred_modes(frame, start_x, start_y, block_size)
            if min_mod != -1:
                mode_freq_list[min_mod] += 1
                if prev_mod == min_mod:
                    mode_pred_list[min_mod] += 1
            prev_mod = min_mod
            # Check Point
            check_frame1[start_y:start_y + block_size, start_x:start_x + block_size] = predicted_block
            # Predicted block is subtracted from source block to get residual block
            residual_block = frame[start_y:start_y + block_size, start_x:start_x + block_size] - predicted_block
            # Check Point
            check_frame2[start_y:start_y + block_size, start_x:start_x + block_size] = residual_block
            # residual block is transformed, quantized, inverse transformed and scaled to reconstruct source block
            residual_block_transformed = dct_transform_block_main(residual_block, qp = qp, block_size = block_size)
            reconstructed_block = predicted_block + residual_block_transformed
            # Check Point
            check_frame3[start_y:start_y + block_size, start_x:start_x + block_size] = reconstructed_block
    # Display the predicted frame for the current mode

    print(f'mode_freq_list: {mode_freq_list}, mode_pred_list: {mode_pred_list}')
    save_frames(frame, filename, "min_sad", qp, check_frame1, check_frame2, check_frame3)


###############################################
# DCT forward and backward Transform functions
def forward_transform(frame):
    # Convert frame to float and normalize pixel values
    frame_float = frame.astype(np.float32) / 255.0
    
    # Apply forward DCT on each block of the frame
    transformed_frame = cv2.dct(frame_float)
    
    return transformed_frame

def backward_transform(transformed_frame):
    # Apply inverse DCT on each block of the transformed frame
    reconstructed_frame = cv2.idct(transformed_frame)
    
    # Convert pixel values back to the original range
    reconstructed_frame = (reconstructed_frame * 255.0).clip(0, 255).astype(np.uint8)
    
    return reconstructed_frame

def quantize_transform(transformed_frame, qp):
    # Calculate quantization step size based on QP value
    quantization_step = np.floor(2.0 ** (qp / 6.0))
    
    # Apply quantization by dividing the transformed coefficients
    quantized_frame = np.round(transformed_frame / quantization_step)
    
    return quantized_frame

def dequantize_transform(quantized_frame, qp):
    # Calculate quantization step size based on QP value
    quantization_step = np.floor(2.0 ** (qp / 6.0))
    
    # Multiply the quantized coefficients with the quantization step
    dequantized_frame = quantized_frame * quantization_step
    
    return dequantized_frame

def dct_transform_block_main(block, qp = 6, block_size = 4):

    # Perform forward transformation
    transformed_block = forward_transform(block)

    # Perform quantization
    quantized_block = quantize_transform(transformed_block, qp)

    # Perform dequantization
    dequantized_block = dequantize_transform(quantized_block, qp)

    # Perform backward transformation
    reconstructed_block = backward_transform(dequantized_block)
    return reconstructed_block

def dct_transform_main(filename, frame_index1, qp = 30, height = 288, width = 352):
    # Load a video frame
    # Load raw YUV frame
#    frame_file = open("input_frame.yuv", "rb")
#    frame_data = frame_file.read()
    frame = read_yuv_file(filename, width, height, frame_index1)
#    frame = cv2.imread('frame.jpg', cv2.IMREAD_GRAYSCALE)

    # Perform forward transformation
    transformed_frame = forward_transform(frame)

    # Perform quantization
    quantized_frame = quantize_transform(transformed_frame, qp)

    # Perform dequantization
    dequantized_frame = dequantize_transform(quantized_frame, qp)

    # Perform backward transformation
    reconstructed_frame = backward_transform(dequantized_frame)

    # Display the original and reconstructed frames
    cv2.imshow('Original Frame', frame)
    cv2.imshow('Reconstructed Frame', reconstructed_frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Main program code
if __name__ == "__main__":

    if len(sys.argv) != 5:
        print("Usage: yuv_reader.py [filename] [height] [width] [block_size]")
        sys.exit(1)

    filename = sys.argv[1]
    height = int(sys.argv[2])
    width = int(sys.argv[3])
    block_size = int(sys.argv[4])

#    if sys.argv[5] not in ['full_search', 'hexbs']:
#         print("Error: unsupported matching method:", sys.argv[5])
#         print("Supported matching methods: full_search, hexbs")
#         sys.exit(1)

    # matching_method = sys.argv[5]

    frame_index1 = 1
#    frame_index2 = 20
#    display_frame(filename, width, height, frame_index1)
#    display_frame(filename, width, height, frame_index2)

    modes_number = 9
    QP_List = [6, 12, 18, 30]
    for qp in QP_List:
        print(f'Run qp: {qp}')
        inter_prediction_blocks_main(filename, frame_index1, qp, block_size = 4, height = 288, width = 352)
    test_intra_pred_modes(filename, frame_index1, qp = 6, block_size = 4, height = 288, width = 352)
#    inter_prediction_yuv_main(filename, frame_index1, block_size = block_size, height = height, width = width)
    # Define the QP value
#    qp = 6
#    dct_transform_main(filename, frame_index1, qp, height = 288, width = 352)

