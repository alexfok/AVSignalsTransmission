import sys
import numpy as np
import matplotlib.pyplot as plt
import cv2

def read_yuv_file(filename, width, height, frame_index):
    # Read the YUV data for a particular frame into a numpy array
    num_pixels = width * height
    with open(filename, "rb") as fp:
        fp.seek(num_pixels * 3 // 2 * frame_index)
        buffer = np.fromfile(fp, dtype=np.uint8, count=num_pixels * 3 // 2)

    # Extract the Y channel and reshape into a 2D array
    y_plane = buffer[:num_pixels].reshape((height, width))

    return y_plane

def calculate_sad(block1, block2):
    # Calculate the sum of absolute differences (SAD) between two blocks
    return np.sum(np.abs(block1 - block2))

def block_matching(frame1, frame2, block_size, search_range):
    # Perform block matching between two frames
    height, width = frame1.shape
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

def display_motion_vectors(filename, width, height, motion_vectors, block_size, scale, frame_index):
    frame = read_yuv_file(filename, width, height, frame_index)
    # Convert the frame to RGB color space
    # frame_rgb = cv2.cvtColor(frame, cv2.COLOR_YUV2RGB_I420)
    # color = (255, 0, 0)

    color = (0, 0, 255)
    radius = 5
    thickness = 2
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
            block_center_x = x
            block_center_y = y
            # x *= scale
            # y *= scale
            # block_center_x = (i + 0.5) * block_size * scale
            # block_center_y = (j + 0.5) * block_size * scale
            start_point = (int(block_center_x), int(block_center_y))
            end_point = (int(block_center_x + x), int(block_center_y + y))
            dx = end_point[0] - start_point[0]
            dy = end_point[1] - start_point[1]
            arrow_length = np.sqrt(dx ** 2 + dy ** 2)
            if arrow_length > arrow_threshold:
                frame = cv2.arrowedLine(frame, start_point, end_point, color, thickness)
                print('draw line start_point: {}, end_point: {}, arrow_length: {}'.format(start_point, end_point, arrow_length))
            else:
                print('Skip draw line, lenght too small: {}'.format(arrow_length))
        else:
            print('block: {}'.format(block))
            not_move_count += 1
            frame = cv2.circle(frame, (x, y), radius, color, circle_thickness)

        """
         x *= scale
        y *= scale
        block_center_x = (i + 0.5) * block_size * scale
        block_center_y = (j + 0.5) * block_size * scale
        start_point = (int(block_center_x), int(block_center_y))
        end_point = (int(block_center_x + x), int(block_center_y + y))

        # Calculate the length of the arrow
        arrow_threshold = 100
        dx = end_point[0] - start_point[0]
        dy = end_point[1] - start_point[1]
        arrow_length = np.sqrt(dx ** 2 + dy ** 2)
        # Draw a point or small circle when the arrow is too small
        print('arrow_length: {}, start_point: {}, end_point: {}'.format(arrow_length, start_point, end_point))
        if arrow_length < arrow_threshold:
#            cv2.circle(frame, (x, y), 1, (255, 0, 0), -1)
            cv2.circle(frame, (x, y), 1, color, -1)
        else:
#            frame = cv2.arrowedLine(frame, start_point, end_point, color, thickness)
            cv2.arrowedLine(frame, start_point, end_point, color, thickness) """
    print('moved blocks count: {}, not moved blocks count: {}'.format(move_count, not_move_count))
    cv2.imshow(f"Motion vectors for frame {frame_index}", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def display_motion_vectors1(filename, width, height, motion_vectors, block_size, scale, frame_index):
    frame = read_yuv_file(filename, width, height, frame_index)
    frame = frame.copy()
    frame_width = frame.shape[1]
    for i in range(motion_vectors.shape[0]):
        for j in range(motion_vectors.shape[1]):
            x, y = motion_vectors[i, j]
            x *= scale
            y *= scale
            block_center_x = (i + 0.5) * block_size * scale
            block_center_y = (j + 0.5) * block_size * scale
            start_point = (int(block_center_x), int(block_center_y))
            end_point = (int(block_center_x + x), int(block_center_y + y))
            color = (0, 0, 255)
            thickness = 1
            frame = cv2.arrowedLine(frame, start_point, end_point, color, thickness)
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

# Main code
if __name__ == "__main__":

    if len(sys.argv) != 6:
        print("Usage: yuv_reader.py [filename] [width] [height] [block_size] [matching_method]")
        sys.exit(1)

    filename = sys.argv[1]
    width = int(sys.argv[2])
    height = int(sys.argv[3])
    block_size = int(sys.argv[4])

    if sys.argv[5] not in ['full_search', 'hexbs']:
        print("Error: unsupported matching method:", sys.argv[5])
        sys.exit(1)

    matching_method = sys.argv[5]

    #matches = frame_matching1(filename, width, height, block_size, matching_method)
    frame_index1 = 0
    frame_index2 = 200
    scale = 0.5
    motion_vectors = frame_matching(filename, width, height, frame_index1, frame_index2, block_size, matching_method)
    display_motion_vectors(filename, width, height, motion_vectors, block_size, scale, frame_index1)
    display_frames_diff(filename, width, height, frame_index1, frame_index2)
