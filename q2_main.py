import sys
import numpy as np
import matplotlib.pyplot as plt
import cv2

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
    print('read_yuv_file2 frame height: {}, width: {}, height1: {}, width1: {}'.format(height, width, height1, width1))

    return y_plane

def calculate_sad(block1, block2):
    # Calculate the sum of absolute differences (SAD) between two blocks
    return np.sum(np.abs(block1 - block2))

def block_matching(frame1, frame2, block_size, search_range):
    # Perform block matching between two frames
    height, width = frame1.shape
    # print('block_matching frame height: {}, width: {}'.format(height, width))
    matches = []
    for i in range(0, height - block_size + 1, block_size):
        for j in range(0, width - block_size + 1, block_size):
            block1 = frame1[i:i+block_size, j:j+block_size]
            min_sad = float('inf')
            best_match = None
            for offset in search_range:
                ii, jj = i + offset[0], j + offset[1]
                if ii >= 0 and ii + block_size <= height and jj >= 0 and jj + block_size <= width:
                    block2 = frame2[ii:ii+block_size, jj:jj+block_size]
                    sad = calculate_sad(block1, block2)
                    if sad < min_sad:
                        min_sad = sad
                        best_match = (ii, jj)
            matches.append(((i, j), best_match, min_sad))
    return matches

def frame_matching(filename, width, height, frame_index1, frame_index2, block_size, matching_method):
    # Read the YUV file and perform block matching between consecutive frames
    matches = []
    frame1 = read_yuv_file(filename, width, height, frame_index1)
    frame2 = read_yuv_file(filename, width, height, frame_index2)
    if matching_method == 'full_search':
        search_range = [(i, j) for i in range(-height // 2 + 1, height // 2) for j in range(-width // 2 + 1, width // 2)]
    elif matching_method == 'hexbs':
        search_range = [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
    else:
        print("Error: unsupported matching method:", matching_method)
        sys.exit(1)
    #print('search_range: {}', search_range)
    #matches.append(block_matching(frame1, frame2, block_size, search_range))
    return block_matching(frame1, frame2, block_size, search_range)
def scale_line(i,j,x,y):
    # x_i = abs(x-i)
    # if abs(x-i) < 5:
    #     x_i = 5
    # y_j = abs(y-j)
    # if abs(y-j) < 5:
    #     y_j = 5

    x_i = i + 5
    y_j = j + 5
    return x_i, y_j
def display_motion_vectors(filename, width, height, motion_vectors, block_size, scale, frame_index):
    frame = read_yuv_file(filename, width, height, frame_index)
    # Convert the frame to RGB color space
    # frame_rgb = cv2.cvtColor(frame, cv2.COLOR_YUV2RGB_I420)
    # color = (255, 0, 0)

    color = (0, 0, 255)
    radius = 2
    thickness = 1
    circle_thickness = 2
    scale = 1
    #motion_vectors = motion_vectors[0]
    move_count = 0
    not_move_count = 0
    arrow_threshold = 200

    for block in motion_vectors:
        (i, j), best_match, min_sad = block
        x, y = best_match
        if (i, j) != (x,y):
            move_count += 1
            x_i, y_j = scale_line(i,j,x,y)
            frame = cv2.arrowedLine(frame, (x_i,y_j), (x,y), color, thickness)
            print('draw line (x_i,y_j) ({},{}), (x,y) ({},{})'.format(x_i,y_j,x,y))
        else:
            print('block: {}'.format(block))
            not_move_count += 1
            frame = cv2.circle(frame, (x, y), radius, color, circle_thickness)

    print('moved blocks count: {}, not moved blocks count: {}'.format(move_count, not_move_count))
    cv2.imshow(f"Motion vectors for frame {frame_index}", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def frame_matching_bad(filename, width, height, frame_index1, frame_index2, block_size, matching_method):
    # Open the YUV file
    yuv_file = open(filename, 'rb')
    
    # Calculate the number of pixels per frame
    frame_size = width * height
    
    # Seek to the start of the desired frames
    yuv_file.seek(frame_index1 * 3 // 2 * frame_size)
    frame1_bytes = yuv_file.read(frame_size)
    yuv_file.seek(frame_index2 * 3 // 2 * frame_size)
    frame2_bytes = yuv_file.read(frame_size)

    # Extract Y channel of the two frames
    frame1_y = np.frombuffer(frame1_bytes, dtype=np.uint8).reshape(height, width)
    frame2_y = np.frombuffer(frame2_bytes, dtype=np.uint8).reshape(height, width)

    # Calculate the difference between the two frames
    diff = np.abs(frame2_y.astype(np.int32) - frame1_y.astype(np.int32)).astype(np.uint8)
    
    # Perform block matching on the Y channel of the frames
    motion_vectors = block_matching(frame1_y, frame2_y, block_size, matching_method)
    
    # Close the YUV file
    yuv_file.close()
    
    # Display the first frame
    plt.subplot(2, 2, 1)
    plt.imshow(frame1_y, cmap='gray')
    plt.title('Frame 1')
    
    # Display the second frame
    plt.subplot(2, 2, 2)
    plt.imshow(frame2_y, cmap='gray')
    plt.title('Frame 2')
    
    # Display the difference between the frames
    plt.subplot(2, 2, 3)
    plt.imshow(diff, cmap='gray')
    plt.title('Difference')
    
    # Display the motion vectors on the first frame
    plt.subplot(2, 2, 4)
    plt.imshow(frame1_y, cmap='gray')
    plt.quiver(
        np.arange(0, width, block_size), 
        np.arange(0, height, block_size), 
        motion_vectors[:, :, 1], 
        motion_vectors[:, :, 0], 
        color='r', 
        units='xy', 
        scale=1
    )
    plt.title('Motion Vectors')
    
    plt.show()

def display_frames_diff(filename, width, height, frame_index1, frame_index2):
    frame1 = read_yuv_file(filename, width, height, frame_index1)
    frame2 = read_yuv_file(filename, width, height, frame_index2)
    # Calculate absolute difference between the two frames
    diff_frame = cv2.absdiff(frame1, frame2)
    # Display the difference frame as an image
    cv2.imshow('Difference Frame', diff_frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def display_frame(filename, width, height, frame_index):
    frame = read_yuv_file(filename, width, height, frame_index)
    cv2.imshow(f"Motion vectors for frame {frame_index}", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Main code
if __name__ == "__main__":

    if len(sys.argv) != 6:
        print("Usage: yuv_reader.py [filename] [height] [width] [block_size] [matching_method]")
        sys.exit(1)

    filename = sys.argv[1]
    height = int(sys.argv[2])
    width = int(sys.argv[3])
    block_size = int(sys.argv[4])

    if sys.argv[5] not in ['full_search', 'hexbs']:
        print("Error: unsupported matching method:", sys.argv[5])
        sys.exit(1)

    matching_method = sys.argv[5]

    #matches = frame_matching1(filename, width, height, block_size, matching_method)
    frame_index1 = 1
    frame_index2 = 2
    scale = 0.5
    display_frame(filename, width, height, frame_index1)
    display_frame(filename, width, height, frame_index2)
    motion_vectors = frame_matching(filename, width, height, frame_index1, frame_index2, block_size, matching_method)
    display_motion_vectors(filename, width, height, motion_vectors, block_size, scale, frame_index2)
#    display_frames_diff(filename, width, height, frame_index1, frame_index2)
#    print(motion_vectors)
