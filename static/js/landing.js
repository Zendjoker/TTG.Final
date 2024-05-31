// preloader.js
document.addEventListener("DOMContentLoaded", function () {
  var chevronDownIcon = document.getElementById("chevron-down-icon");
  var ProfileDropDown = document.getElementById("profile-dropdown");
  var containerProfile = document.querySelector(".container-profile");

  ProfileDropDown.addEventListener("click", function () {
    chevronDownIcon.classList.toggle("rotate");
    containerProfile.style.display =
      containerProfile.style.display === "flex" ? "none" : "flex";
  });
});

document.addEventListener("DOMContentLoaded", function () {
  const dropdownMenu = document.getElementById("dropDownMenu");
  const navLinks = document.querySelectorAll(".menu-item");
  const hamburgerLines = document.querySelector(".hamburger-lines");
  const navToggle = document.getElementById("navToggle");

  navToggle.addEventListener("change", function () {
    if (this.checked) {
      hamburgerLines.classList.add("checked");
      dropdownMenu.style.transform = "translate(0)";
      dropdownMenu.style.zIndex = "1";
    } else {
      hamburgerLines.classList.remove("checked");
      dropdownMenu.style.transform = "translate(-150%)";
    }
  });
  // Close the menu when a menu item is clicked
  navLinks.forEach(function (link) {
    link.addEventListener("click", function () {
      dropdownMenu.style.transform = "translate(-150%)";
      hamburgerLines.classList.remove("checked");
    });
  });
});

document.addEventListener("DOMContentLoaded", function () {
  var notification = document.querySelector(".notification");
  var notificationMenu = document.querySelector(".notification > .menu");
  var messages = document.querySelector(".messages");
  var messagesMenu = document.querySelector(".messages > .menu");
  var body = document.querySelector("body");

  if (notification && notificationMenu) {
    notification.addEventListener("click", function (e) {
      e.stopPropagation();
      closeMenu(messages);
      toggleMenu(notification);
    });

    notificationMenu.addEventListener("click", function (e) {
      e.stopPropagation();
    });
  } else {
    console.error("Notification or NotificationMenu not found.");
  }

  if (messages && messagesMenu) {
    messages.addEventListener("click", function (e) {
      e.stopPropagation();
      closeMenu(notification);
      toggleMenu(messages);
    });

    messagesMenu.addEventListener("click", function (e) {
      e.stopPropagation();
    });
  } else {
    console.error("Messages or MessagesMenu not found.");
  }

  body.addEventListener("click", function () {
    closeAllMenu();
  });

  function toggleMenu(displayTarget) {
    var navigationList = [displayTarget.classList.item(0)];

    navigationList.forEach(function (item) {
      var element = document.querySelector(`.${item}`);
      if (element) {
        element.classList.toggle("--active");
      } else {
        console.error(`Element with class ${item} not found.`);
      }
    });
  }

  function closeAllMenu() {
    var navigationList = ["notification", "messages"];

    navigationList.forEach(function (item) {
      var element = document.querySelector(`.${item}`);
      if (element && element.classList.contains("--active")) {
        element.classList.remove("--active");
      }
    });
  }

  function closeMenu(menuToClose) {
    var element = document.querySelector(`.${menuToClose.classList.item(0)}`);
    if (element && element.classList.contains("--active")) {
      element.classList.remove("--active");
    }
  }
});

document.addEventListener("DOMContentLoaded", function () {
  const rootElement = document.getElementById("preloader");
  const preloader = document.createElement("div");
  preloader.innerHTML = getPreloaderHTML();
  rootElement.appendChild(preloader);

  const preloaderTimeout = setTimeout(() => {
    rootElement.removeChild(preloader);
    clearTimeout(preloaderTimeout);
  }, 6000);
});

function getPreloaderHTML() {
  return `<div class="loader">
        <div class="load-text">
          <div class="loaded-text">T</div>
          <div class="loading-text">
            unisian
            <img src="../static/assets/preloader.png" alt="hustle-logo" />
            Hustlers
          </div>
        </div>
        <div class="m-load-text">
          <div class="m-loaded-text">Tunisian</div>
          <div class="m-loading-text">
            <img src="../static/assets/preloader.png" alt="hustle-logo" />
            Hustlers
          </div>
        </div>
      </div>`;
}

// Function to set course details

function setCourseDetails(type) {
  const devSelected = type === "dev";
  const tradeSelected = type === "trade";
  const coursesContainer = document.querySelector(".courses-container");
  

  // Handle logic based on devSelected and tradeSelected
  if (devSelected) {
    document.querySelector(".courses-container").innerHTML = `
          <div class="details-wrapper"> 
          <div class="details">
            <div class="details-container">
            <button class="goBack">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-move-left"><path d="M6 8L2 12L6 16"/><path d="M2 12H22"/></svg>
            Go Back
            </button>
                <div class="details-title">
                    <span>Money  Making From Trading</span>
                    <span>700DT/ Monthly</span>
                </div>
                <div class="details-content">
                    <div class="details-access">
                        <p>You will Get Access to:</p>
                        <p style={{textAlign: "start"}}>
                            Gain access to an extensive library of over 50 video courses and carefully 
                            organized tutorials, encompassing topics ranging from the basics of 
                            contemporary trading to specialized, profit-generating strategies .
                        </p>
                    </div>
                    <div class="details-features">
                        <span>
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-check-check"><path d="M18 6 7 17l-5-5"/><path d="m22 10-7.5 7.5L13 16"/></svg>&nbsp; Simple-step-by-step tutorials
                        </span>
                        <span>
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-check-check"><path d="M18 6 7 17l-5-5"/><path d="m22 10-7.5 7.5L13 16"/></svg>&nbsp; Easy-to-follow program for financial success
                        </span>
                        <span>
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-check-check"><path d="M18 6 7 17l-5-5"/><path d="m22 10-7.5 7.5L13 16"/></svg>&nbsp; Community chat groups
                        </span>
                        <span>
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-check-check"><path d="M18 6 7 17l-5-5"/><path d="m22 10-7.5 7.5L13 16"/></svg>&nbsp; No experience Needed
                        </span>
                        <span>
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-check-check"><path d="M18 6 7 17l-5-5"/><path d="m22 10-7.5 7.5L13 16"/></svg>&nbsp; Live Trade , Market News
                        </span>
                        <span>
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-check-check"><path d="M18 6 7 17l-5-5"/><path d="m22 10-7.5 7.5L13 16"/></svg>&nbsp; 2 wealth creation methods
                        </span>
                        <span>
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-check-check"><path d="M18 6 7 17l-5-5"/><path d="m22 10-7.5 7.5L13 16"/></svg>&nbsp; Super advanced learning Platform
                        </span>
                    </div>
                </div>
                <div class="details-footer">
                    <div class="details-button"><span>Get Started Now</span></div>
                    <div class="students">
                        <div>
                        <img
                            src="../static/assets/studentsImg.png"
                            alt="devimg"
                            width={200}
                            height={200}
                            layout="responsive"
                            />
                        </div>
                        <div>
                            <span>Join 100+ students</span>
                        </div>
                        
                    </div>
                </div>
  
            </div>
            </div>
            </div>`;
  } else if (tradeSelected) {
    document.querySelector(".courses-container").innerHTML = `
          <div class="details-wrapper"> 
          <div class="details">
            <div class="details-container">
            <button class="goBack">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-move-left"><path d="M6 8L2 12L6 16"/><path d="M2 12H22"/></svg>
            Go Back
            </button>
                <div class="details-title">
                    <span>Money  Making From Trading</span>
                    <span>700DT/ Monthly</span>
                </div>
                <div class="details-content">
                    <div class="details-access">
                        <p>You will Get Access to:</p>
                        <p style={{textAlign: "start"}}>
                            Gain access to an extensive library of over 50 video courses and carefully 
                            organized tutorials, encompassing topics ranging from the basics of 
                            contemporary trading to specialized, profit-generating strategies .
                        </p>
                    </div>
                    <div class="details-features">
                        <span>
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-check-check"><path d="M18 6 7 17l-5-5"/><path d="m22 10-7.5 7.5L13 16"/></svg>&nbsp; Simple-step-by-step tutorials
                        </span>
                        <span>
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-check-check"><path d="M18 6 7 17l-5-5"/><path d="m22 10-7.5 7.5L13 16"/></svg>&nbsp; Easy-to-follow program for financial success
                        </span>
                        <span>
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-check-check"><path d="M18 6 7 17l-5-5"/><path d="m22 10-7.5 7.5L13 16"/></svg>&nbsp; Community chat groups
                        </span>
                        <span>
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-check-check"><path d="M18 6 7 17l-5-5"/><path d="m22 10-7.5 7.5L13 16"/></svg>&nbsp; No experience Needed
                        </span>
                        <span>
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-check-check"><path d="M18 6 7 17l-5-5"/><path d="m22 10-7.5 7.5L13 16"/></svg>&nbsp; Live Trade , Market News
                        </span>
                        <span>
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-check-check"><path d="M18 6 7 17l-5-5"/><path d="m22 10-7.5 7.5L13 16"/></svg>&nbsp; 2 wealth creation methods
                        </span>
                        <span>
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-check-check"><path d="M18 6 7 17l-5-5"/><path d="m22 10-7.5 7.5L13 16"/></svg>&nbsp; Super advanced learning Platform
                        </span>
                    </div>
                </div>
                <div class="details-footer">
                    <div class="details-button"><span>Get Started Now</span></div>
                    <div class="students">
                        <div>
                        <img
                            src="../static/assets/studentsImg.png"
                            alt="devimg"
                            width={200}
                            height={200}
                            layout="responsive"
                            />
                        </div>
                        <div>
                            <span>Join 100+ students</span>
                        </div>
                        
                    </div>
                </div>
  
            </div>
            </div>
            </div>`;
  }
  const goBackButton = document.querySelector(".goBack");
  goBackButton.addEventListener("click", function () {
    // Reset course details
    coursesContainer.innerHTML = `      <div class="courses-container">
    <div class="cr-container" onclick="setCourseDetails('trade')">
      <div class="cr-content">
        <span class="h2-text">Money Making From Trading</span>
        <div class="cr-learn-more">
          <span class="p-text">
            Learn More &nbsp;
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" data-lucide="move-right" class="lucide lucide-move-right"><path d="M18 8L22 12L18 16"></path><path d="M2 12H22"></path></svg>
          </span>
        </div>
      </div>
      <div class="cr-images">
        <img
          src="/static/assets/trade-img.png"
          alt="tradeimg"
          width="480"
          height="269"
        />
      </div>
    </div>
    <div class="cr-container not-allowed">
    <div class="cr-content">
      <span class="h2-text">The Development Journey</span>
      <div class="cr-learn-more">
        <span class="p-text">
          Learn More &nbsp;
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" data-lucide="move-right" class="lucide lucide-move-right"><path d="M18 8L22 12L18 16"></path><path d="M2 12H22"></path></svg>
        </span>
      </div>
    </div>
    <div class="cr-images">
      <img
        src="/static/assets/dev-img.png"
        alt="devimg"
        width="480"
        height="269"
      />
    </div>
  </div>
  </div>`;
    // Or you can set it to some default content
    // coursesContainer.innerHTML = "<div>Default content</div>";
  });
};
// Get the button
var scrollToTopBtn = document.getElementById("scrollToTopBtn");

// When the user scrolls down 100px from the top of the document, show the button
window.onscroll = function() {scrollFunction()};

function scrollFunction() {
  if (document.body.scrollTop > 100 || document.documentElement.scrollTop > 100) {
    scrollToTopBtn.classList.add("show");
  } else {
    scrollToTopBtn.classList.remove("show");
  }
}

// When the user clicks on the button, scroll to the top of the document
scrollToTopBtn.addEventListener("click", function() {
  window.scrollTo({ top: 0, behavior: 'smooth' });
});


document.addEventListener("DOMContentLoaded", function () {
  const feedbacksImgContainer = document.getElementById(
    "feedbacksImgContainer"
  );
  const feedbackOrder = [];

  const feedbacks = [
    { id: 1, imagePath: "../static/assets/feedback1.svg" },
    { id: 2, imagePath: "../static/assets/feedback2.svg" },
    { id: 3, imagePath: "../static/assets/feedback3.svg" },
  ];

  const initialPositions = [
    { bottom: "-5%", left: "25%", zIndex: 2, position: "absolute" },
    { bottom: "6%", right: "17%", zIndex: 1, position: "absolute" },
    { bottom: "16%", left: "17%", zIndex: 0, position: "absolute" },
  ];

  feedbacks.forEach((feedback, index) => {
    const feedbackImg = document.createElement("div");
    feedbackImg.className = "feedback-img";
    feedbackImg.style.opacity = "0";
    feedbackImg.innerHTML = `<img src="${feedback.imagePath}" alt="Feedback ${feedback.id}" width="622" height="484">`;

    Object.assign(feedbackImg.style, initialPositions[index]); // Set initial positions

    feedbackOrder.push(feedbackImg);
    feedbacksImgContainer.appendChild(feedbackImg);

    feedbackImg.addEventListener("click", function () {
      moveFeedback(feedbackImg);
    });

    setTimeout(() => (feedbackImg.style.opacity = "1"), 100);
  });

  function moveFeedback(selectedFeedback) {
    const selectedIndex = feedbackOrder.indexOf(selectedFeedback);
    if (selectedIndex !== -1) {
      feedbackOrder.unshift(feedbackOrder.splice(selectedIndex, 1)[0]);
      updateFeedbackPositions();
    } else {
      console.error("Selected feedback not found in the order array");
    }
  }

  function updateFeedbackPositions() {
    feedbackOrder.forEach((feedbackImg, index) => {
      const position =
        initialPositions[index] ||
        initialPositions[initialPositions.length - 1];

      // Apply the new positions
      Object.assign(feedbackImg.style, {
        zIndex: position.zIndex,
        bottom: position.bottom,
        left: position.left || "auto",
        right: position.right || "auto",
      });

      // Add 'visible' class for the top image and remove for others
      if (index === 0) {
        feedbackImg.classList.add("visible");
      } else {
        feedbackImg.classList.remove("visible");
      }
    });
  }
});

const images = [
];

const sliderContainer = document.getElementById("sliderContainer");
const slider = document.getElementById("slider");

let currentIndex = 0;

const updateSlider = () => {
  slider.style.transform = `translateX(-${currentIndex * 10}%)`;
};

const interval = setInterval(() => {
  currentIndex = (currentIndex + 1) % images.length;
  updateSlider();
}, 1500);


images.forEach((image, index) => {
  const imgElement = document.createElement("img");
  imgElement.src = image;
  imgElement.alt = `StudentWins ${index}`;
  imgElement.className = "sliderImage";
  slider.appendChild(imgElement);
});


images.forEach((image, index) => {
  const imgElement = document.createElement("img");
  imgElement.src = image;
  imgElement.alt = `Slide ${index}`;
  imgElement.className = "sliderImage";
  slider.appendChild(imgElement);
});

const reverseImages = [
];

const reverseSliderContainer = document.getElementById(
  "reverseSliderContainer"
);
const reverseSlider = document.getElementById("reverseSlider");

let reverseCurrentIndex = 0;

const updateReverseSlider = () => {
  reverseCurrentIndex = (reverseCurrentIndex - 1 + reverseImages.length) % reverseImages.length;
  reverseSlider.style.transform = `translateX(-${reverseCurrentIndex * 10}%)`;
};

const ReverseInterval = setInterval(() => {
  updateReverseSlider();
}, 1500);

reverseImages.forEach((image, index) => {
  const imgElement = document.createElement("img");
  imgElement.src = image;
  imgElement.alt = `StudentWins ${index}`;
  imgElement.className = "sliderImage";
  reverseSlider.appendChild(imgElement);
});

document.addEventListener("DOMContentLoaded", function () {
  const dropdownMenu = document.getElementById("dropDownMenu");
  const navLinks = document.querySelectorAll(".menu-item");
  const hamburgerLines = document.querySelector(".hamburger-lines");
  const navToggle = document.getElementById("navToggle");
  const navContainer = document.getElementById("navContainer");

  navToggle.addEventListener("change", function () {
    if (this.checked) {
      hamburgerLines.classList.add("checked");
      dropdownMenu.style.transform = "translate(0)";
      dropdownMenu.style.zIndex = "1";
      navContainer.style.position = "fixed";
      navContainer.style.zIndex = "100";

    } else {
      hamburgerLines.classList.remove("checked");
      dropdownMenu.style.transform = "translate(-150%)";
      navContainer.style.position = "relative";
      navContainer.style.zIndex = "100";

    }
  });
  // Close the menu when a menu item is clicked
  navLinks.forEach(function (link) {
    link.addEventListener("click", function () {
      dropdownMenu.style.transform = "translate(-150%)";
      hamburgerLines.classList.remove("checked");
    });
  });
});






