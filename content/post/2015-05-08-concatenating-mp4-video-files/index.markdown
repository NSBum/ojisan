---
layout: post
title: "Concatenating mp4 video files"
date: 2015-05-08 05:36:51 -0500
aliases: ['/2015/05/08/concatenating-mp4-video-files/']
comments: true
categories:
- miscellaneous
tags:
- tutorial
- video
---
I recently shot a recital with my Sony A7. While it's a wonderful camera for stills and it produces some excellent video too, cameras like this are not meant for continuous video recording. There are limitations that are imposed by compression algorithm licensing requirements. And, it seems, there are limits that are imposed by thermal issues inside the camera.

To make a long story short, my A7 ended up giving me two video files instead of one for this event. What to do?

First I thought of making a round-trip through iMovie; but I so dislike that confusing dumbed-down piece of software that I'd rather doing anything other than that. Fortunately I stumbled upon `ffmpeg`.

### Installing Homebrew and `ffmpeg`

On OS X, the easiest way to install `ffmpeg` is to use [Homebrew](http://brew.sh). I do. I'm not going to walk through all of the steps for installing Homebrew as they are published [elsewhere](http://brew.sh).

After installing Homebrew, you'll need to install `ffmpeg`. I followed [another set of instructions](http://www.renevolution.com/how-to-install-ffmpeg-on-mac-os-x/). I started by looking at all of the installation options available for `ffmpeg`:

{{< highlight bash >}}
~|⇒ brew options ffmpeg
{{< /highlight >}}

Not being a audio/video codec guy, I found it too confusing; so I cut and pasted the command to install `ffmpeg` with all of the options:

{{< highlight bash >}}
brew install ffmpeg --with-fdk-aac --with-ffplay --with-freetype --with-frei0r --with-libass --with-libvo-aacenc --with-libvorbis --with-libvpx --with-opencore-amr --with-openjpeg --with-opus --with-rtmpdump --with-schroedinger --with-speex --with-theora --with-tools
{{< /highlight >}}

### Concatenating files with `ffmpeg`

Now, you need to create a text file specifying the videos that you wish to join. The paths are relative to the text file path. So, I created a text file on the desktop and called it concatv.txt:

{{< highlight bash >}}
# videos to concatenate
file '2015_04_11_13_49_29.mp4'
file '2015_04_11_13_59_42.mp4'
{{< /highlight >}}

Now, go to the Terminal (or iTerm like I use) and give the concatenation command for `ffmpeg` with your specification file and the output location and options:

{{< highlight bash >}}
~|⇒ ffmpeg -f concat -i ~/Desktop/concatv.txt -acodec ac3 -vcodec copy output.mp4

ffmpeg version 2.5 Copyright (c) 2000-2014 the FFmpeg developers
  built on May  7 2015 06:08:38 with Apple LLVM version 6.1.0 (clang-602.0.49) (based on LLVM 3.6.0svn)
  configuration: --prefix=/usr/local/Cellar/ffmpeg/2.5 --enable-shared --enable-pthreads --enable-gpl --enable-version3 --enable-hardcoded-tables --enable-avresample --cc=clang --host-cflags= --host-ldflags= --enable-libx264 --enable-libmp3lame --enable-libxvid --enable-libfreetype --enable-libtheora --enable-libvorbis --enable-libvpx --enable-librtmp --enable-libopencore-amrnb --enable-libopencore-amrwb --enable-libvo-aacenc --enable-libass --enable-ffplay --enable-libspeex --enable-libschroedinger --enable-libfdk-aac --enable-libopus --enable-frei0r --enable-libopenjpeg --disable-decoder=jpeg2000 --extra-cflags='-I/usr/local/Cellar/openjpeg/1.5.1_1/include/openjpeg-1.5 ' --enable-nonfree --enable-vda
  libavutil      54. 15.100 / 54. 15.100
  libavcodec     56. 13.100 / 56. 13.100
  libavformat    56. 15.102 / 56. 15.102
  libavdevice    56.  3.100 / 56.  3.100
  libavfilter     5.  2.103 /  5.  2.103
  libavresample   2.  1.  0 /  2.  1.  0
  libswscale      3.  1.101 /  3.  1.101
  libswresample   1.  1.100 /  1.  1.100
  libpostproc    53.  3.100 / 53.  3.100
Input #0, concat, from '/Users/alan/Desktop/concatv.txt':
  Duration: N/A, start: 0.000000, bitrate: 15957 kb/s
    Stream #0:0: Video: h264 (High) (avc1 / 0x31637661), yuv420p(tv, bt709), 1920x1080 [SAR 1:1 DAR 16:9], 15704 kb/s, 29.97 fps, 29.97 tbr, 30k tbn, 59.94 tbc
    Stream #0:1: Audio: aac (LC) (mp4a / 0x6134706D), 48000 Hz, stereo, fltp, 253 kb/s
Output #0, mp4, to 'output.mp4':
  Metadata:
    encoder         : Lavf56.15.102
    Stream #0:0: Video: h264 ([33][0][0][0] / 0x0021), yuv420p, 1920x1080 [SAR 1:1 DAR 16:9], q=2-31, 15704 kb/s, 29.97 fps, 30k tbn, 30k tbc
    Stream #0:1: Audio: ac3 ([165][0][0][0] / 0x00A5), 48000 Hz, stereo, fltp, 192 kb/s
    Metadata:
      encoder         : Lavc56.13.100 ac3
Stream mapping:
  Stream #0:0 -> #0:0 (copy)
  Stream #0:1 -> #0:1 (aac (native) -> ac3 (native))
Press [q] to stop, [?] for help
frame= 1660 fps=0.0 q=-1.0 size=  170730kB time=00:00:55.35 bitrate=25266.2kbits/frame= 3300 fps=3299 q=-1.0 size=  338567kB time=00:01:50.07 bitrate=25196.4kbitsframe= 4820 fps=3213 q=-1.0 size=  494783kB time=00:02:40.79 bitrate=25207.8kbitsframe= 6470 fps=3235 q=-1.0 size=  663576kB time=00:03:35.84 bitrate=25184.3kbitsframe= 7880 fps=3152 q=-1.0 size=  808522kB time=00:04:22.89 bitrate=25194.0kbitsframe= 9520 fps=3173 q=-1.0 size=  977105kB time=00:05:17.62 bitrate=25200.8kbitsframe=10920 fps=3119 q=-1.0 size= 1120948kB time=00:06:04.34 bitrate=25203.5kbitsframe=12660 fps=3164 q=-1.0 size= 1298599kB time=00:07:02.38 bitrate=25185.6kbitsframe=14279 fps=3172 q=-1.0 size= 1464549kB time=00:07:56.40 bitrate=25183.4kbitsframe=16030 fps=3205 q=-1.0 size= 1644149kB time=00:08:54.83 bitrate=25183.3kbitsframe=17880 fps=3248 q=-1.0 size= 1833635kB time=00:09:56.56 bitrate=25179.5kbitsframe=19530 fps=3251 q=-1.0 size= 2004140kB time=00:10:51.64 bitrate=25194.7kbitsframe=21080 fps=3239 q=-1.0 size= 2162571kB time=00:11:43.33 bitrate=25188.2kbitsframe=22920 fps=3271 q=-1.0 size= 2351215kB time=00:12:44.73 bitrate=25186.9kbitsframe=24378 fps=3247 q=-1.0 size= 2500568kB time=00:13:33.37 bitrate=25184.6kbitsframe=26090 fps=3258 q=-1.0 size= 2676095kB time=00:14:30.50 bitrate=25183.8kbitsframe=27840 fps=3272 q=-1.0 size= 2856249kB time=00:15:28.89 bitrate=25189.5kbitsframe=29570 fps=3279 q=-1.0 size= 3032933kB time=00:16:26.61 bitrate=25182.8kbitsframe=31130 fps=3271 q=-1.0 size= 3178060kB time=00:17:18.67 bitrate=25065.4kbitsframe=35330 fps=3527 q=-1.0 size= 3182691kB time=00:19:38.81 bitrate=22117.7kbitsframe=39660 fps=3771 q=-1.0 size= 3187472kB time=00:22:03.28 bitrate=19732.5kbitsframe=43280 fps=3928 q=-1.0 size= 3191459kB time=00:24:04.07 bitrate=18104.6kbitsframe=47660 fps=4138 q=-1.0 size= 3196297kB time=00:26:30.22 bitrate=16465.7kbitsframe=50265 fps=4183 q=-1.0 size= 3288092kB time=00:27:57.18 bitrate=16060.2kbitsframe=51955 fps=4151 q=-1.0 size= 3461672kB time=00:28:53.57 bitrate=16358.1kbitsframe=53695 fps=4125 q=-1.0 size= 3640451kB time=00:29:51.63 bitrate=16645.4kbitsframe=55075 fps=4074 q=-1.0 size= 3782069kB time=00:30:37.69 bitrate=16859.6kbitsframe=56841 fps=4055 q=-1.0 size= 3962677kB time=00:31:36.60 bitrate=17116.0kbitsframe=58625 fps=4038 q=-1.0 size= 4145422kB time=00:32:36.13 bitrate=17360.4kbitsframe=60221 fps=4010 q=-1.0 size= 4309072kB time=00:33:29.38 bitrate=17567.5kbitsframe=61865 fps=3986 q=-1.0 size= 4478416kB time=00:34:24.25 bitrate=17772.6kbitsframe=63675 fps=3975 q=-1.0 size= 4663684kB time=00:35:24.63 bitrate=17981.9kbitsframe=65371 fps=3957 q=-1.0 size= 4837570kB time=00:36:21.22 bitrate=18168.4kbitsframe=66712 fps=3920 q=-1.0 size= 4975079kB time=00:37:05.96 bitrate=18309.3kbitsframe=69115 fps=3945 q=-1.0 size= 5090248kB time=00:38:26.14 bitrate=18081.8kbitsframe=73456 fps=4077 q=-1.0 size= 5095040kB time=00:40:51.00 bitrate=17029.2kbitsframe=77825 fps=4202 q=-1.0 size= 5099858kB time=00:43:16.77 bitrate=16088.4kbitsframe=82205 fps=4322 q=-1.0 size= 5104691kB time=00:45:42.91 bitrate=15245.7kbitsframe=86583 fps=4436 q=-1.0 size= 5109513kB time=00:48:08.99 bitrate=14488.5kbitsframe=90945 fps=4543 q=-1.0 size= 5114326kB time=00:50:34.54 bitrate=13806.5kbitsframe=95295 fps=4644 q=-1.0 size= 5119122kB time=00:52:59.68 bitrate=13188.7kbitsframe=98790 fps=4719 q=-1.0 Lsize= 5125570kB time=00:54:56.37 bitrate=12737.8kbits/s
video:5045729kB audio:77259kB subtitle:0kB other streams:0kB global headers:0kB muxing overhead: 0.050416%
{{< /highlight >}}

And you're done.
