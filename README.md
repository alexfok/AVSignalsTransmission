# TODO
- switch cli to argparse
- add partial frame draw:
  - not moved blocks
  - moved blocks on new positions
- test display_motion_vectors function - do not draw arrows\circles, only plain frame
# Python
pip install opencv-python
# Run main:
python ./q2_main.py waterfall_cif.yuv 288 352 8 hexbs


## ffplay
### download
https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl-shared.zip 
###  run
./ffmpeg-master-latest-win64-gpl/bin/ffplay -f rawvideo -pixel_format yuv420p -video_size 1920x1080 road_movie_1920x1080_25.yuv
./ffmpeg-master-latest-win64-gpl/bin/ffplay -f rawvideo -pixel_format yuv420p -video_size 352x288 ./stv/waterfall_cif.yuv

<!---
[rawvideo @ 00000116a3dff180] Estimating duration from bitrate, this may be inaccurate
Input #0, rawvideo, from 'road_movie_1920x1080_25.yuv':
  Duration: 00:00:30.00, start: 0.000000, bitrate: 622080 kb/s
  Stream #0:0: Video: rawvideo (I420 / 0x30323449), yuv420p, 1920x1080, 622080 kb/s, 25 tbr, 25 tbn
  33.01 M-V:  0.023 fd=   2 aq=    0KB vq=    0KB sq=    0B f=0/0
 
-->
## kvazaar
### download
https://github.com/ultravideo/kvazaar#docker
https://docs.docker.com/engine/install/
docker pull ultravideo/kvazaar 
### Run kvazaar container
docker run -i -a STDIN -a STDOUT ultravideo/kvazaar -i - --input-res=1920x1080 -o - < road_movie_1920x1080_25.yuv > out.265

./kvazaar.exe --input waterfall_cif.yuv --output waterfall.hevc --input-res=352x288
./kvazaar.exe --input road_movie_1920x1080_25.yuv --input-res=1920x1080 --output road_movie.hevc

Input: waterfall_cif.yuv, output: waterfall.hevc
  Video size: 1920x1080 (input=1920x1080)
Processed 12 frames,   74855528 bits AVG PSNR Y 38.9601 U 38.7163 V 38.7247
 Total CPU time: 8.438 s.
 Encoding time: 8.430 s.
 Encoding wall time: 8.429 s.
 Encoding CPU usage: 100.00%
 FPS: 1.42
 Bitrate: 148.725 Mbps
 AVG QP: 24.1

# Q1
## tz
./kvazaar.exe --input road_movie_1920x1080_25.yuv --input-res=1920x1080 --output road_movie_tz.hevc --me tz --bitrate 4000000
 Input: road_movie_1920x1080_25.yuv, output: road_movie_tz.hevc
  Video size: 1920x1080 (input=1920x1080)
 Processed 750 frames,  123512920 bits AVG PSNR Y 32.1232 U 41.3855 V 42.1544
 Total CPU time: 119.480 s.
 Encoding time: 119.086 s.
 Encoding wall time: 119.086 s.
 Encoding CPU usage: 100.00%
 FPS: 6.30
 Bitrate: 3.926 Mbps
 AVG QP: 38.2

## hexbs
./kvazaar.exe --input road_movie_1920x1080_25.yuv --input-res=1920x1080 --output road_movie_hexbs.hevc --me hexbs --bitrate 4000000
 Input: road_movie_1920x1080_25.yuv, output: road_movie_hexbs.hevc
  Video size: 1920x1080 (input=1920x1080)
 Processed 750 frames,  123436824 bits AVG PSNR Y 31.9923 U 41.3491 V 42.1204
 Total CPU time: 127.073 s.
 Encoding time: 126.152 s.
 Encoding wall time: 126.152 s.
 Encoding CPU usage: 100.00%
 FPS: 5.95
 Bitrate: 3.924 Mbps
 AVG QP: 38.5

## dia
./kvazaar.exe --input road_movie_1920x1080_25.yuv --input-res=1920x1080 --output road_movie_dia.hevc --me dia --bitrate 4000000
 Processed 750 frames,  123686720 bits AVG PSNR Y 32.0134 U 41.3658 V 42.1407
 Total CPU time: 140.403 s.
 Encoding time: 139.975 s.
 Encoding wall time: 139.975 s.
 Encoding CPU usage: 100.00%
 FPS: 5.36
 Bitrate: 3.932 Mbps
 AVG QP: 38.4

## full
./kvazaar.exe --input road_movie_1920x1080_25.yuv --input-res=1920x1080 --output road_movie_full.hevc --me full --bitrate 4000000
 Processed 750 frames,  123626704 bits AVG PSNR Y 32.1875 U 41.3575 V 42.1622
 Total CPU time: 796.435 s.
 Encoding time: 796.426 s.
 Encoding wall time: 796.426 s.
 Encoding CPU usage: 100.00%
 FPS: 0.94
 Bitrate: 3.930 Mbps
 AVG QP: 38.2

# Q2

Motion Vectors:
python ./q2_main.py ./stv/akiyo_cif.yuv 288 352 16 hexbs
akiyo_16_1_2
frame_index1 = 1
frame_index2 = 2
moved blocks count: 63, not moved blocks count: 333

akiyo_16_1_20
frame_index1 = 1
frame_index2 = 20
moved blocks count: 141, not moved blocks count: 255


./kvazaar.exe --input waterfall_cif.yuv --output waterfall.hevc --input-res=352x288
yuv_reader.py [filename] [width] [height] [block_size] [matching_method]
python ./yuv_reader_block_match.py waterfall_cif.yuv 352 288 8 hexbs

# Q3 B
      --subme <integer>      : Fractional pixel motion estimation level [4]
                                   - 0: Integer motion estimation only
                                   - 1: + 1/2-pixel horizontal and vertical
                                   - 2: + 1/2-pixel diagonal
                                   - 3: + 1/4-pixel horizontal and vertical
                                   - 4: + 1/4-pixel diagonal

## hexbs
./kvazaar.exe --input road_movie_1920x1080_25.yuv --input-res=1920x1080 --output road_movie_hexbs.hevc --me hexbs --bitrate 1000000 --subme 0
 Input: road_movie_1920x1080_25.yuv, output: road_movie_hexbs.hevc
  Video size: 1920x1080 (input=1920x1080)
 Processed 750 frames,  123436824 bits AVG PSNR Y 31.9923 U 41.3491 V 42.1204
 Total CPU time: 31.442 s.
 Encoding time: 31.435 s.
 Encoding wall time: 31.434 s.
 Encoding CPU usage: 100.00%
 FPS: 23.86
 Bitrate: 0.951 Mbps
 AVG QP: 46.4

./kvazaar.exe --input road_movie_1920x1080_25.yuv --input-res=1920x1080 --output road_movie_hexbs.hevc --me hexbs --bitrate 1000000 --subme 1
  Processed 750 frames,   29932248 bits AVG PSNR Y 27.6941 U 38.1197 V 38.9464
Total CPU time: 45.566 s.
 Encoding time: 45.560 s.
 Encoding wall time: 45.560 s.
 Encoding CPU usage: 100.00%
 FPS: 16.46
 Bitrate: 0.952 Mbps
 AVG QP: 46.2

./kvazaar.exe --input road_movie_1920x1080_25.yuv --input-res=1920x1080 --output road_movie_hexbs.hevc --me hexbs --bitrate 1000000 --subme 2
 Processed 750 frames,   29910432 bits AVG PSNR Y 27.7300 U 38.0613 V 38.8895
 Total CPU time: 46.429 s.
 Encoding time: 46.423 s.
 Encoding wall time: 46.424 s.
 Encoding CPU usage: 100.00%
 FPS: 16.16
 Bitrate: 0.951 Mbps
 AVG QP: 46.1

./kvazaar.exe --input road_movie_1920x1080_25.yuv --input-res=1920x1080 --output road_movie_hexbs.hevc --me hexbs --bitrate 1000000 --subme 3
 Processed 750 frames,   29921712 bits AVG PSNR Y 27.8057 U 38.0966 V 38.9033
 Total CPU time: 45.194 s.
 Encoding time: 45.187 s.
 Encoding wall time: 45.188 s.
 Encoding CPU usage: 100.00%
 FPS: 16.60
 Bitrate: 0.951 Mbps
 AVG QP: 46.0

./kvazaar.exe --input road_movie_1920x1080_25.yuv --input-res=1920x1080 --output road_movie_hexbs.hevc --me hexbs --bitrate 1000000 --subme 4
 Processed 750 frames,   29896224 bits AVG PSNR Y 27.8264 U 38.0779 V 38.9277
 Total CPU time: 45.099 s.
 Encoding time: 45.093 s.
 Encoding wall time: 45.092 s.
 Encoding CPU usage: 100.00%
 FPS: 16.63
 Bitrate: 0.950 Mbps
 AVG QP: 45.9

./kvazaar.exe --input road_movie_1920x1080_25.yuv --input-res=1920x1080 --output road_movie_hexbs.hevc --me hexbs --bitrate 2000000 --subme 0
 Processed 750 frames,   60951912 bits AVG PSNR Y 29.1462 U 39.7932 V 40.5347
 Total CPU time: 61.695 s.
 Encoding time: 61.687 s.
 Encoding wall time: 61.688 s.
 Encoding CPU usage: 100.00%
 FPS: 12.16
 Bitrate: 1.938 Mbps
 AVG QP: 43.3

./kvazaar.exe --input road_movie_1920x1080_25.yuv --input-res=1920x1080 --output road_movie_hexbs.hevc --me hexbs --bitrate 2000000 --subme 1
 Processed 750 frames,   60973408 bits AVG PSNR Y 29.2749 U 39.9103 V 40.6920
 Total CPU time: 51.431 s.
 Encoding time: 51.424 s.
 Encoding wall time: 51.424 s.
 Encoding CPU usage: 100.00%
 FPS: 14.58
 Bitrate: 1.938 Mbps
 AVG QP: 43.3

./kvazaar.exe --input road_movie_1920x1080_25.yuv --input-res=1920x1080 --output road_movie_hexbs.hevc --me hexbs --bitrate 2000000 --subme 2
 Processed 750 frames,   60971208 bits AVG PSNR Y 29.3272 U 39.9398 V 40.7763
 Total CPU time: 65.645 s.
 Encoding time: 65.640 s.
 Encoding wall time: 65.640 s.
 Encoding CPU usage: 100.00%
 FPS: 11.43
 Bitrate: 1.938 Mbps
 AVG QP: 43.3

./kvazaar.exe --input road_movie_1920x1080_25.yuv --input-res=1920x1080 --output road_movie_hexbs.hevc --me hexbs --bitrate 2000000 --subme 3
 Processed 750 frames,   60985976 bits AVG PSNR Y 29.4951 U 39.9671 V 40.8345
 Total CPU time: 72.507 s.
 Encoding time: 72.501 s.
 Encoding wall time: 72.501 s.
 Encoding CPU usage: 100.00%
 FPS: 10.34
 Bitrate: 1.939 Mbps
 AVG QP: 43.0

./kvazaar.exe --input road_movie_1920x1080_25.yuv --input-res=1920x1080 --output road_movie_hexbs.hevc --me hexbs --bitrate 2000000 --subme 4
 Processed 750 frames,   60929096 bits AVG PSNR Y 29.4935 U 39.9461 V 40.8241
 Total CPU time: 75.421 s.
 Encoding time: 75.405 s.
 Encoding wall time: 75.405 s.
 Encoding CPU usage: 100.00%
 FPS: 9.95
 Bitrate: 1.937 Mbps
 AVG QP: 43.1

./kvazaar.exe --input road_movie_1920x1080_25.yuv --input-res=1920x1080 --output road_movie_hexbs.hevc --me hexbs --bitrate 4000000 --subme 0
 Processed 750 frames,  122950168 bits AVG PSNR Y 31.4268 U 41.1370 V 41.8587
 Total CPU time: 86.871 s.
 Encoding time: 86.864 s.
 Encoding wall time: 86.864 s.
 Encoding CPU usage: 100.00%
 FPS: 8.63
 Bitrate: 3.908 Mbps
 AVG QP: 39.1

./kvazaar.exe --input road_movie_1920x1080_25.yuv --input-res=1920x1080 --output road_movie_hexbs.hevc --me hexbs --bitrate 4000000 --subme 1
 Processed 750 frames,  123711560 bits AVG PSNR Y 31.8085 U 41.3179 V 42.0576
 Total CPU time: 86.468 s.
 Encoding time: 86.460 s.
 Encoding wall time: 86.460 s.
 Encoding CPU usage: 100.00%
 FPS: 8.67
 Bitrate: 3.933 Mbps
 AVG QP: 38.6

./kvazaar.exe --input road_movie_1920x1080_25.yuv --input-res=1920x1080 --output road_movie_hexbs.hevc --me hexbs --bitrate 4000000 --subme 2
 Processed 750 frames,  123588248 bits AVG PSNR Y 31.8542 U 41.3205 V 42.0614
 Total CPU time: 91.119 s.
 Encoding time: 91.112 s.
 Encoding wall time: 91.111 s.
 Encoding CPU usage: 100.00%
 FPS: 8.23
 Bitrate: 3.929 Mbps
 AVG QP: 38.6

./kvazaar.exe --input road_movie_1920x1080_25.yuv --input-res=1920x1080 --output road_movie_hexbs.hevc --me hexbs --bitrate 4000000 --subme 3
 Processed 750 frames,  123055168 bits AVG PSNR Y 32.0123 U 41.3490 V 42.0968
 Total CPU time: 89.423 s.
 Encoding time: 89.416 s.
 Encoding wall time: 89.416 s.
 Encoding CPU usage: 100.00%
 FPS: 8.39
 Bitrate: 3.912 Mbps
 AVG QP: 38.4

./kvazaar.exe --input road_movie_1920x1080_25.yuv --input-res=1920x1080 --output road_movie_hexbs.hevc --me hexbs --bitrate 4000000 --subme 4
 Processed 750 frames,  123436824 bits AVG PSNR Y 31.9923 U 41.3491 V 42.1204
 Total CPU time: 93.985 s.
 Encoding time: 93.978 s.
 Encoding wall time: 93.977 s.
 Encoding CPU usage: 100.00%
 FPS: 7.98
 Bitrate: 3.924 Mbps
 AVG QP: 38.5

./kvazaar.exe --input road_movie_1920x1080_25.yuv --input-res=1920x1080 --output road_movie_hexbs.hevc --me hexbs --bitrate 8000000 --subme 0
 Processed 750 frames,  246602312 bits AVG PSNR Y 34.2411 U 42.4859 V 43.0789
 Total CPU time: 109.243 s.
 Encoding time: 109.237 s.
 Encoding wall time: 109.238 s.
 Encoding CPU usage: 100.00%
 FPS: 6.87
 Bitrate: 7.839 Mbps
 AVG QP: 34.4

./kvazaar.exe --input road_movie_1920x1080_25.yuv --input-res=1920x1080 --output road_movie_hexbs.hevc --me hexbs --bitrate 8000000 --subme 1
 Processed 750 frames,  248678320 bits AVG PSNR Y 34.7159 U 42.6736 V 43.2748
 Total CPU time: 116.183 s.
 Encoding time: 116.173 s.
 Encoding wall time: 116.170 s.
 Encoding CPU usage: 100.00%
 FPS: 6.46
 Bitrate: 7.905 Mbps
 AVG QP: 33.8

./kvazaar.exe --input road_movie_1920x1080_25.yuv --input-res=1920x1080 --output road_movie_hexbs.hevc --me hexbs --bitrate 8000000 --subme 2
 Processed 750 frames,  248564864 bits AVG PSNR Y 34.8338 U 42.7232 V 43.3140
 Total CPU time: 121.666 s.
 Encoding time: 121.657 s.
 Encoding wall time: 121.651 s.
 Encoding CPU usage: 100.00%
 FPS: 6.17
 Bitrate: 7.902 Mbps
 AVG QP: 33.6

./kvazaar.exe --input road_movie_1920x1080_25.yuv --input-res=1920x1080 --output road_movie_hexbs.hevc --me hexbs --bitrate 8000000 --subme 3
 Processed 750 frames,  245641288 bits AVG PSNR Y 34.9014 U 42.7284 V 43.3366
 Total CPU time: 122.462 s.
 Encoding time: 122.453 s.
 Encoding wall time: 122.454 s.
 Encoding CPU usage: 100.00%
 FPS: 6.12
 Bitrate: 7.809 Mbps
 AVG QP: 33.6

./kvazaar.exe --input road_movie_1920x1080_25.yuv --input-res=1920x1080 --output road_movie_hexbs.hevc --me hexbs --bitrate 8000000 --subme 4
 Processed 750 frames,  246158448 bits AVG PSNR Y 34.9563 U 42.7223 V 43.3380
 Total CPU time: 131.026 s.
 Encoding time: 131.017 s.
 Encoding wall time: 131.017 s.
 Encoding CPU usage: 100.00%
 FPS: 5.72
 Bitrate: 7.825 Mbps
 AVG QP: 33.5



## Usage
$ docker run -i -a STDIN -a STDOUT ultravideo/kvazaar
Usage:
kvazaar -i <input> --input-res <width>x<height> -o <output>

Required:
  -i, --input <filename>     : Input file
      --input-res <res>      : Input resolution [auto]
                                   - auto: Detect from file name.
                                   - <int>x<int>: width times height
  -o, --output <filename>    : Output file

Presets:
      --preset <preset>      : Set options to a preset [medium]
                                   - ultrafast, superfast, veryfast, faster,
                                     fast, medium, slow, slower, veryslow
                                     placebo

Input:
  -n, --frames <integer>     : Number of frames to code [all]
      --seek <integer>       : First frame to code [0]
      --input-fps <num>[/<denom>] : Frame rate of the input video [25]
      --source-scan-type <string> : Source scan type [progressive]
                                   - progressive: Progressive scan
                                   - tff: Top field first
                                   - bff: Bottom field first
      --input-format <string> : P420 or P400 [P420]
      --input-bitdepth <int> : 8-16 [8]
      --loop-input           : Re-read input file forever.

Options:
      --help                 : Print this help message and exit.
      --version              : Print version information and exit.
      --(no-)aud             : Use access unit delimiters. [disabled]
      --debug <filename>     : Output internal reconstruction.
      --(no-)cpuid           : Enable runtime CPU optimizations. [enabled]
      --hash <string>        : Decoded picture hash [checksum]
                                   - none: 0 bytes
                                   - checksum: 18 bytes
                                   - md5: 56 bytes
      --(no-)psnr            : Calculate PSNR for frames. [enabled]
      --(no-)info            : Add encoder info SEI. [enabled]
      --crypto <string>      : Selective encryption. Crypto support must be
                               enabled at compile-time. Can be 'on' or 'off' or
                               a list of features separated with a '+'. [off]
                                   - on: Enable all encryption features.
                                   - off: Disable selective encryption.
                                   - mvs: Motion vector magnitudes.
                                   - mv_signs: Motion vector signs.
                                   - trans_coeffs: Coefficient magnitudes.
                                   - trans_coeff_signs: Coefficient signs.
                                   - intra_pred_modes: Intra prediction modes.
      --key <string>         : Encryption key [16,213,27,56,255,127,242,112,
                                               97,126,197,204,25,59,38,30]

Video structure:
  -q, --qp <integer>         : Quantization parameter [22]
  -p, --period <integer>     : Period of intra pictures [64]
                                   - 0: Only first picture is intra.
                                   - 1: All pictures are intra.
                                   - N: Every Nth picture is intra.
      --vps-period <integer> : How often the video parameter set is re-sent [0]
                                   - 0: Only send VPS with the first frame.
                                   - N: Send VPS with every Nth intra frame.
  -r, --ref <integer>        : Number of reference frames, in range 1..15 [4]
      --gop <string>         : GOP structure [8]
                                   - 0: Disabled
                                   - 8: B-frame pyramid of length 8
                                   - lp-<string>: Low-delay P-frame GOP
                                     (e.g. lp-g8d4t2, see README)
      --(no-)open-gop        : Use open GOP configuration. [enabled]
      --cqmfile <filename>   : Read custom quantization matrices from a file.
      --scaling-list <string>: Set scaling list mode. [off]
                                   - off: Disable scaling lists.
                                   - custom: use custom list (with --cqmfile).
                                   - default: Use default lists.
      --bitrate <integer>    : Target bitrate [0]
                                   - 0: Disable rate control.
                                   - N: Target N bits per second.
      --(no-)lossless        : Use lossless coding. [disabled]
      --mv-constraint <string> : Constrain movement vectors. [none]
                                   - none: No constraint
                                   - frametile: Constrain within the tile.
                                   - frametilemargin: Constrain even more.
      --roi <filename>       : Use a delta QP map for region of interest.
                               Reads an array of delta QP values from a text
                               file. The file format is: width and height of
                               the QP delta map followed by width*height delta
                               QP values in raster order. The map can be of any
                               size and will be scaled to the video size.
      --set-qp-in-cu         : Set QP at CU level keeping pic_init_qp_minus26.
                               in PPS zero.
      --(no-)erp-aqp         : Use adaptive QP for 360 degree video with
                               equirectangular projection. [disabled]
      --level <number>       : Use the given HEVC level in the output and give
                               an error if level limits are exceeded. [6.2]
                                   - 1, 2, 2.1, 3, 3.1, 4, 4.1, 5, 5.1, 5.2, 6,
                                     6.1, 6.2
      --force-level <number> : Same as --level but warnings instead of errors.
      --high-tier            : Used with --level. Use high tier bitrate limits
                               instead of the main tier limits during encoding.
                               High tier requires level 4 or higher.

Compression tools:
      --(no-)deblock <beta:tc> : Deblocking filter. [0:0]
                                   - beta: Between -6 and 6
                                   - tc: Between -6 and 6
      --sao <string>         : Sample Adaptive Offset [full]
                                   - off: SAO disabled
                                   - band: Band offset only
                                   - edge: Edge offset only
                                   - full: Full SAO
      --(no-)rdoq            : Rate-distortion optimized quantization [enabled]
      --(no-)rdoq-skip       : Skip RDOQ for 4x4 blocks. [disabled]
      --(no-)signhide        : Sign hiding [disabled]
      --(no-)smp             : Symmetric motion partition [disabled]
      --(no-)amp             : Asymmetric motion partition [disabled]
      --rd <integer>         : Intra mode search complexity [0]
                                   - 0: Skip intra if inter is good enough.
                                   - 1: Rough intra mode search with SATD.
                                   - 2: Refine intra mode search with SSE.
                                   - 3: Try all intra modes and enable intra
                                        chroma mode search.
      --(no-)mv-rdo          : Rate-distortion optimized motion vector costs
                               [disabled]
      --(no-)full-intra-search : Try all intra modes during rough search.
                               [disabled]
      --(no-)transform-skip  : Try transform skip [disabled]
      --me <string>          : Integer motion estimation algorithm [hexbs]
                                   - hexbs: Hexagon Based Search
                                   - tz:    Test Zone Search
                                   - full:  Full Search
                                   - full8, full16, full32, full64
                                   - dia:   Diamond Search
      --me-steps <integer>   : Motion estimation search step limit. Only
                               affects 'hexbs' and 'dia'. [-1]
      --subme <integer>      : Fractional pixel motion estimation level [4]
                                   - 0: Integer motion estimation only
                                   - 1: + 1/2-pixel horizontal and vertical
                                   - 2: + 1/2-pixel diagonal
                                   - 3: + 1/4-pixel horizontal and vertical
                                   - 4: + 1/4-pixel diagonal
      --pu-depth-inter <int>-<int> : Inter prediction units sizes [0-3]
                                   - 0, 1, 2, 3: from 64x64 to 8x8
      --pu-depth-intra <int>-<int> : Intra prediction units sizes [1-4]
                                   - 0, 1, 2, 3, 4: from 64x64 to 4x4
      --tr-depth-intra <int> : Transform split depth for intra blocks [0]
      --(no-)bipred          : Bi-prediction [disabled]
      --cu-split-termination <string> : CU split search termination [zero]
                                   - off: Don't terminate early.
                                   - zero: Terminate when residual is zero.
      --me-early-termination <string> : Motion estimation termination [on]
                                   - off: Don't terminate early.
                                   - on: Terminate early.
                                   - sensitive: Terminate even earlier.
      --fast-residual-cost <int> : Skip CABAC cost for residual coefficients
                                   when QP is below the limit. [0]
      --(no-)intra-rdo-et    : Check intra modes in rdo stage only until
                               a zero coefficient CU is found. [disabled]
      --(no-)implicit-rdpcm  : Implicit residual DPCM. Currently only supported
                               with lossless coding. [disabled]
      --(no-)tmvp            : Temporal motion vector prediction [enabled]

Parallel processing:
      --threads <integer>    : Number of threads to use [auto]
                                   - 0: Process everything with main thread.
                                   - N: Use N threads for encoding.
                                   - auto: Select automatically.
      --owf <integer>        : Frame-level parallelism [auto]
                                   - N: Process N+1 frames at a time.
                                   - auto: Select automatically.
      --(no-)wpp             : Wavefront parallel processing. [enabled]
                               Enabling tiles automatically disables WPP.
                               To enable WPP with tiles, re-enable it after
                               enabling tiles. Enabling wpp with tiles is,
                               however, an experimental feature since it is
                               not supported in any HEVC profile.
      --tiles <int>x<int>    : Split picture into width x height uniform tiles.
      --tiles-width-split <string>|u<int> :
                                   - <string>: A comma-separated list of tile
                                               column pixel coordinates.
                                   - u<int>: Number of tile columns of uniform
                                             width.
      --tiles-height-split <string>|u<int> :
                                   - <string>: A comma-separated list of tile row
                                               column pixel coordinates.
                                   - u<int>: Number of tile rows of uniform
                                             height.
      --slices <string>      : Control how slices are used.
                                   - tiles: Put tiles in independent slices.
                                   - wpp: Put rows in dependent slices.
                                   - tiles+wpp: Do both.

Video Usability Information:
      --sar <width:height>   : Specify sample aspect ratio
      --overscan <string>    : Specify crop overscan setting [undef]
                                   - undef, show, crop
      --videoformat <string> : Specify video format [undef]
                                   - undef, component, pal, ntsc, secam, mac
      --range <string>       : Specify color range [tv]
                                   - tv, pc
      --colorprim <string>   : Specify color primaries [undef]
                                   - undef, bt709, bt470m, bt470bg,
                                     smpte170m, smpte240m, film, bt2020
      --transfer <string>    : Specify transfer characteristics [undef]
                                   - undef, bt709, bt470m, bt470bg,
                                     smpte170m, smpte240m, linear, log100,
                                     log316, iec61966-2-4, bt1361e,
                                     iec61966-2-1, bt2020-10, bt2020-12
      --colormatrix <string> : Specify color matrix setting [undef]
                                   - undef, bt709, fcc, bt470bg, smpte170m,
                                     smpte240m, GBR, YCgCo, bt2020nc, bt2020c
      --chromaloc <integer>  : Specify chroma sample location (0 to 5) [0]

Deprecated parameters: (might be removed at some point)
  -w, --width <integer>       : Use --input-res.
  -h, --height <integer>      : Use --input-res.
