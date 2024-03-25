document.addEventListener("DOMContentLoaded", function() {
  /**
   * HomePage - Help section
   */
  class Help {
    constructor($el) {
      this.$el = $el;
      this.$buttonsContainer = $el.querySelector(".help--buttons");
      this.$slidesContainers = $el.querySelectorAll(".help--slides");
      this.currentSlide = this.$buttonsContainer.querySelector(".active").parentElement.dataset.id;
      this.init();
    }

    init() {
      this.events();
    }

    events() {
      /**
       * Slide buttons
       */
      this.$buttonsContainer.addEventListener("click", e => {
        if (e.target.classList.contains("btn")) {
          this.changeSlide(e);
        }
      });

      /**
       * Pagination buttons
       */
      this.$el.addEventListener("click", e => {
        if (e.target.classList.contains("btn") && e.target.parentElement.parentElement.classList.contains("help--slides-pagination")) {
          this.changePage(e);
        }
      });
    }

    changeSlide(e) {
      e.preventDefault();
      const $btn = e.target;

      // Buttons Active class change
      [...this.$buttonsContainer.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
      $btn.classList.add("active");

      // Current slide
      this.currentSlide = $btn.parentElement.dataset.id;

      // Slides active class change
      this.$slidesContainers.forEach(el => {
        el.classList.remove("active");

        if (el.dataset.id === this.currentSlide) {
          el.classList.add("active");
        }
      });
    }

    /**
     * TODO: callback to page change event
     */
    changePage(e) {
      e.preventDefault();
      const page = e.target.dataset.page;

      console.log(page);
    }
  }

  const helpSection = document.querySelector(".help");
  if (helpSection !== null) {
    new Help(helpSection);
  }

  /**
   * Form Select
   */
  class FormSelect {
    constructor($el) {
      this.$el = $el;
      this.options = [...$el.children];
      this.init();
    }

    init() {
      this.createElements();
      this.addEvents();
      this.$el.parentElement.removeChild(this.$el);
    }

    createElements() {
      // Input for value
      this.valueInput = document.createElement("input");
      this.valueInput.type = "text";
      this.valueInput.name = this.$el.name;

      // Dropdown container
      this.dropdown = document.createElement("div");
      this.dropdown.classList.add("dropdown");

      // List container
      this.ul = document.createElement("ul");

      // All list options
      this.options.forEach((el, i) => {
        const li = document.createElement("li");
        li.dataset.value = el.value;
        li.innerText = el.innerText;

        if (i === 0) {
          // First clickable option
          this.current = document.createElement("div");
          this.current.innerText = el.innerText;
          this.dropdown.appendChild(this.current);
          this.valueInput.value = el.value;
          li.classList.add("selected");
        }

        this.ul.appendChild(li);
      });

      this.dropdown.appendChild(this.ul);
      this.dropdown.appendChild(this.valueInput);
      this.$el.parentElement.appendChild(this.dropdown);
    }

    addEvents() {
      this.dropdown.addEventListener("click", e => {
        const target = e.target;
        this.dropdown.classList.toggle("selecting");

        // Save new value only when clicked on li
        if (target.tagName === "LI") {
          this.valueInput.value = target.dataset.value;
          this.current.innerText = target.innerText;
        }
      });
    }
  }

  document.querySelectorAll(".form-group--dropdown select").forEach(el => {
    new FormSelect(el);
  });

  /**
   * Hide elements when clicked on document
   */
  document.addEventListener("click", function (e) {
    const target = e.target;
    const tagName = target.tagName;

    if (target.classList.contains("dropdown")) return false;

    if (tagName === "LI" && target.parentElement.parentElement.classList.contains("dropdown")) {
      return false;
    }

    if (tagName === "DIV" && target.parentElement.classList.contains("dropdown")) {
      return false;
    }

    document.querySelectorAll(".form-group--dropdown .dropdown").forEach(el => {
      el.classList.remove("selecting");
    });
  });

  /**
   * Switching between form steps
   */
  class FormSteps {
  constructor(form) {
    this.$form = form;
    this.$next = form.querySelectorAll(".next-step");
    this.$prev = form.querySelectorAll(".prev-step");
    this.$step = form.querySelector(".form--steps-counter span");
    this.currentStep = 1;

    this.$stepInstructions = form.querySelectorAll(".form--steps-instructions p");
    const $stepForms = form.querySelectorAll("form > div");
    this.slides = [...this.$stepInstructions, ...$stepForms];

    this.init();
  }

  init() {
    this.events();
    this.updateForm();
  }

  events() {
    // Next step
    this.$next.forEach(btn => {
      btn.addEventListener("click", e => {
        e.preventDefault();
        this.currentStep++;
        this.updateForm();
      });
    });

    // Previous step
    this.$prev.forEach(btn => {
      btn.addEventListener("click", e => {
        e.preventDefault();
        this.currentStep--;
        this.updateForm();
      });
    });

    // Form submit
    this.$form.querySelector("form").addEventListener("submit", e => this.submit(e));

    // Filter institutions based on selected categories
    const categories = document.querySelectorAll('input[name="categories"]');
    const institutions = document.querySelectorAll('.form-group--checkbox');

    categories.forEach(category => {
      category.addEventListener('change', () => {
        const selectedCategories = Array.from(categories).filter(cat => cat.checked).map(cat => cat.value);
        institutions.forEach(institution => {
          const institutionCategoriesAttr = institution.getAttribute('data-categories');
          if (institutionCategoriesAttr) {
            const institutionCategories = institutionCategoriesAttr.split(',');
            if (selectedCategories.some(cat => institutionCategories.includes(cat))) {
              institution.style.display = 'block';
            } else {
              institution.style.display = 'none';
            }
          }
        });
      });
    });
  }

  updateForm() {
    this.$step.innerText = this.currentStep;

    this.slides.forEach(slide => {
      slide.classList.remove("active");

      if (slide.dataset.step == this.currentStep) {
        slide.classList.add("active");
      }
    });

    this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
    this.$step.parentElement.hidden = this.currentStep >= 6;

    if (this.currentStep === 5) {
      this.displaySummary();
    }
  }

  displaySummary() {
    const formData = new FormData(this.$form.querySelector("form"));
    document.getElementById("summary-bags").textContent = formData.get("bags") + " worek/ów z darami";
    document.getElementById("summary-organization").textContent = `Dla  "${formData.get("organization")}"`;
    document.getElementById("summary-address").textContent = formData.get("address");
    document.getElementById("summary-city").textContent = formData.get("city");
    document.getElementById("summary-postcode").textContent = formData.get("postcode");
    document.getElementById("summary-phone").textContent = formData.get("phone");
    document.getElementById("summary-date").textContent = formData.get("data");
    document.getElementById("summary-time").textContent = formData.get("time");
    document.getElementById("summary-more-info").textContent = formData.get("more_info");
  }

  submit(e) {

  e.preventDefault();

  const formData = new FormData(this.$form.querySelector("form"));
  const data = {
    quantity: formData.get("bags"),
    categories: formData.getAll("categories"),
    institution: formData.get("organization"),
    address: formData.get("address"),
    phone_number: formData.get("phone"),
    city: formData.get("city"),
    zip_code: formData.get("postcode"),
    pick_up_date: formData.get("data"),
    pick_up_time: formData.get("time"),
    pick_up_comment: formData.get("more_info")
  };

  const csrfToken = getCookie("csrftoken");
  fetch('/add_donation/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken
    },
    body: JSON.stringify(data)
  })
  .then(response => {
    if (!response.ok) {
      throw new Error('Wystąpił błąd podczas przetwarzania żądania.');
    }
    return response.json();
  })
      .then(data => {

    console.log(data);
    window.location.href = data.redirect_url;
})
  .then(data => {

    console.log(data);
  })
  .catch(error => {
    console.error('Błąd:', error);
  });
}
}
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();}

const form = document.querySelector(".form--steps");
if (form !== null) {
  new FormSteps(form);
}
})
