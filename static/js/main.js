$(document).ready(function(){
  let namespace = "/test";
  let video = document.querySelector("#videoElement");
  let canvas = document.querySelector("#canvasElement");
  let ctx = canvas.getContext('2d');

  var localMediaStream = null;
  var detectaudio=null

  var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);

  var quality = 0.5;

  function sendSnapshot() {
    if (!localMediaStream) {
      return;
    }

    ctx.drawImage(video, 0, 0, video.videoWidth, video.videoHeight, 0, 0, 320, 180);

    let dataURL = canvas.toDataURL('image/jpeg', quality);
    socket.emit('input image', dataURL);
  }

  function sendAudio() {
    if (!localMediaStream) {
      return;
    }
    socket.emit('input audio', Math.round(detectaudio*100));
  }

  function better_quality() {
    if (quality < 0.7) quality = quality + 0.1;
  }

  function worse_quality() {
    if (quality > 0.2) quality = quality - 0.1;
  }

  socket.on('connect', function() {
    console.log('Connected!');
  });

  update_quality = function(output_length, process_length){
    console.log("Output List: " + output_length + ", process_list: " + process_length);
    if (output_length >= 1 || process_length >= 1)
      worse_quality();
    else if (output_length == 0 && process_length == 0)
      better_quality();
    console.log('Current quality: ' + quality);
  };

  var constraints = {
    audio: true,
    video: {
      width: { min: 640 },
      height: { min: 360 }
    }
  };

  navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
    video.srcObject = stream;
    localMediaStream = stream;
    var  context = new AudioContext();
    var  liveSource = context.createMediaStreamSource(stream);
    var levelChecker = context.createScriptProcessor(1024,1,1);
    liveSource.connect(levelChecker);
    levelChecker.connect(context.destination);
    levelChecker.onaudioprocess = function(e) {
      var buffer = e.inputBuffer.getChannelData(0);
      var maxVal = 0;
      for (var i = 0; i < buffer.length; i++) {
        if (maxVal < buffer[i]) {
          maxVal = buffer[i];
        }
        detectaudio = maxVal;
      }
    };

    var sendcount = 0;
    setInterval(function () {
      sendSnapshot();
      sendcount = sendcount + 1;
      if (sendcount >= 20) {
        socket.emit('request condition', 3, update_quality);
        sendcount = 0;
      }
      sendAudio();
    }, 50);
  }).catch(function(error) {console.log(error);});
});

