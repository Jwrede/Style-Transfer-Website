$("#page").scrollspy();

(function () {
  var body = document.body,
    e = document.documentElement,
    scrollPercent;
  $(window)
    .unbind("scroll")
    .scroll(function () {
      scrollPercent =
        (100 * $(window).scrollTop()) /
        ($(document).height() - $(window).height());
      body.style.backgroundPosition = "0px " + scrollPercent + "%";
    });
})();

document.onscroll = function () {
  document.getElementById("curr_page").textContent = $(
    ".nav-link.active"
  ).text();
};

function rangeSlide(value, page) {
  document.getElementById("rangeValue" + page).innerHTML = parseFloat(value)
    .toFixed(2)
    .toLocaleString();
}

function acceptImage(event, output_div) {
  var input = event.target;
  var reader = new FileReader();
  reader.onload = function () {
    var dataURL = reader.result;
    var output = document.getElementById(output_div);
    output.src = dataURL;
  };
  reader.readAsDataURL(input.files[0]);
}

function StyleIT(page) {
  let content_image = document
    .getElementById("content-image" + page)
    .src.split(",")[1];
  let style_image = document
    .getElementById("style-image" + page)
    .src.split(",")[1];
  let resolution1 = document.getElementById("drop" + page).value.split("x")[0];
  let resolution2 = document.getElementById("drop" + page).value.split("x")[1];
  let alpha = document.getElementById("input-slider" + page).value;
  let preserve_color = $(`input[name='check${page}']`).is(":checked");

  req = $.ajax({
    url: "/style_image",
    type: "POST",
    data: {
      content: content_image,
      style: style_image,
      resolution1: resolution1,
      resolution2: resolution2,
      alpha: alpha,
      preserve_color: preserve_color,
    },
  });
  req.done(function (data) {
    document.getElementById("result-image" + page).src =
      "data:image/png;base64," + data.result;
    console.log("data:image/png;base64," + data.result);
  });
}

function downloadImage(target) {
  resultIMG = document.getElementById(target).src;
  download(resultIMG, "result.png", "image/png");
}

function randomImage(id, type) {
  var input = event.target;
  var reader = new FileReader();
  reader.onload = function () {
    var dataURL = reader.result;
    var output = document.getElementById(id);
    output.src = dataURL;
  };
  reader.readAsDataURL(input.files[0]);
}

function rotateImage(target_image) {
  document.getElementById(target_image).style.transition = "0.5s";
  if (document.getElementById(target_image).style.width === "50%") {
    document.getElementById(target_image).style.width = "100%";
  } else {
    document.getElementById(target_image).style.width = "50%";
  }
  setTimeout(function () {
    document.getElementById(target_image).style.transition = "none";
  }, 500);
}

function randomImage(id, type) {
  req = $.ajax({
    url: "/random",
    type: "POST",
    data: {
      type: type,
    },
  });
  req.done(function (data) {
    document.getElementById(id).src = "data:image/png;base64," + data.img;
  });
}

new Vue({
  delimiters: ["[[", "]]"],
  el: "#style-images-wrapper",
  data: {
    images: [
      {
        image:
      },
      {
        image:
      },
    ],
  },
  methods: {
    add: function (event) {
      if (this.images.length <= 8) {
        var that = this.images;
        var input = event.target;
        var reader = new FileReader();
        reader.onload = function () {
          var dataURL = reader.result;
          var output = that.push({ image: dataURL });
        };
        reader.readAsDataURL(input.files[0]);
      } else {
        alert("Maximum of 8 style images");
      }
    },
    random: function () {
      if (this.images.length <= 8) {
        var that = this.images;
        req = $.ajax({
          url: "/random",
          type: "POST",
          data: {
            type: "style",
          },
        });
        req.done(function (data) {
          var output = that.push({
            image: "data:image/png;base64," + data.img,
          });
        });
      } else {
        alert("Maximum of 8 style images");
      }
    },
    remove: function () {
      if ($(".carousel-item").length > 0) {
        var index = $(".carousel-item.active").index();
        if (
          index === $(".carousel-item").length - 1 &&
          $(".carousel-item").length > 1
        ) {
          $(".carousel-item")[$(".carousel-item").length - 2].classList.add(
            "active"
          );
          $(".slide-pages")[$(".carousel-item").length - 2].classList.add(
            "active"
          );
        }
        this.images.splice(index, 1);
      } else {
        alert("No Images to remove!");
      }
    },
    StyleIT: function () {
      if (this.images.length === 0) {
        alert("No style images selected!");
      } else {
        let content_image = document
          .getElementById("content-image2")
          .src.split(",")[1];
        let resolution1 = document.getElementById("drop2").value.split("x")[0];
        let resolution2 = document.getElementById("drop2").value.split("x")[1];
        let alpha = document.getElementById("input-slider2").value;
        let preserve_color = $(`input[name='check2']`).is(":checked");

        let styles = [];
        for (var i of this.images) {
          console.log(i.image);
          styles.push(i.image.split(",")[1]);
        }

        req = $.ajax({
          url: "/style_interpolation",
          type: "POST",
          data: {
            content: content_image,
            styles: styles,
            resolution1: resolution1,
            resolution2: resolution2,
            alpha: alpha,
            preserve_color: preserve_color,
          },
        });
        req.done(function (data) {
          document.getElementById("result-image2").src =
            "data:image/png;base64," + data.result;
          console.log("data:image/png;base64," + data.result);
        });
      }
    },
  },
});

$(".carousel").on("touchstart", function (event) {
  var xClick = event.originalEvent.touches[0].pageX;
  $(this).one("touchmove", function (event) {
    var xMove = event.originalEvent.touches[0].pageX;
    if (Math.floor(xClick - xMove) > 5) {
      $(this).carousel("next");
    } else if (Math.floor(xClick - xMove) < -5) {
      $(this).carousel("prev");
    }
  });
  $(".carousel").on("touchend", function () {
    $(this).off("touchmove");
  });
});

function acceptVideo(event, output_div) {
  var input = event.target;
  var reader = new FileReader();
  reader.onload = function () {
    var dataURL = reader.result;
    var output = document.getElementById(output_div);
    output.src = dataURL;
  };
  reader.readAsDataURL(input.files[0]);
}

function StyleITVideo() {
  let content_image = document
    .getElementById("content-video")
    .src.split(",")[1];
  let style_image = document.getElementById("style-image3").src.split(",")[1];
  let resolution1 = document.getElementById("drop3").value.split("x")[0];
  let resolution2 = document.getElementById("drop3").value.split("x")[1];
  let alpha = document.getElementById("input-slider3").value;
  let preserve_color = $(`input[name='check3']`).is(":checked");

  let content_video = document.getElementById("select-content3").files[0];
  console.log(document.getElementById("select-content3").files[0]);
  let formData = new FormData();
  formData.append("content", content_video);

  req = $.ajax({
    url: "/style_video",
    type: "POST",
    data: formData,
    contentType: false,
    processData: false,
  });
  req.done(function (data) {
    console.log("ye");
  });
}