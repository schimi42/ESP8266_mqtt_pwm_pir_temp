camera:
  - platform: generic
    still_image_url: http://192.168.2.195/cgi-bin/currentpic.cgi
    name: cam_xia5

shell_command:
  camxia5_1: wget http://192.168.2.195/cgi-bin/currentpic.cgi -O /tmp/xia5_1.jpg
  camxia5_2: wget http://192.168.2.195/cgi-bin/currentpic.cgi -O /tmp/xia5_2.jpg
  camxia5_3: wget http://192.168.2.195/cgi-bin/currentpic.cgi -O /tmp/xia5_3.jpg
  camxia5_4: wget http://192.168.2.195/cgi-bin/currentpic.cgi -O /tmp/xia5_4.jpg
  camxia5_5: wget http://192.168.2.195/cgi-bin/currentpic.cgi -O /tmp/xia5_5.jpg