document.addEventListener("DOMContentLoaded", function () {
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

        /**
         * Init all methods
         */
        init() {
            this.events();
            this.updateForm();
        }

        /**
         * All events that are happening in form
         */
        events() {
            // Next step
            this.$next.forEach(btn => {
                btn.addEventListener("click", e => {
                    e.preventDefault();
                    if (this.selectedCategory().length === 0) {
                        this.showErrorOnButton(e.target, "Musisz wybrać kategorie")
                    } else if (this.currentStep === 2 && this.amountOfBags() === '') {
                        this.showErrorOnButton(e.target, "Podaj ile worków chcesz przekazać ")
                    } else if (this.currentStep === 3 && this.selectedInstitution() === undefined) {
                        this.showErrorOnButton(e.target, "Wybierz instytucje do obdarowania.")
                    } else if (this.currentStep === 4 && this.checkReceiptForm() === undefined) {
                        this.showErrorOnButton(e.target, "Usupełnij wszystkie pola");
                    } else {
                        this.currentStep++;
                        this.updateForm();
                    }

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
        }

        selectedCategory() {
            const categorySet = $(this.slides[4]).find('input[name="categories"]:checked'),
                result = [];
            categorySet.each(function (id, element) {
                result.push(element.value)
            });
            return result;
        }

        amountOfBags() {
            return $(this.slides[5]).find('input[name="bags"]').val()
        }

        selectedInstitution() {

            return $(this.slides[6]).find('input[name="organization"]:checked')[0];
        }

        checkReceiptForm() {
            const inputs = $(this.slides[7]).find('input'),
                result = {};
            try {
                inputs.map(function (id, element) {
                    if ($(element).val() === '') {
                        throw 'EmptyValue';
                    } else {
                        result[element.name] = element.value;
                    }
                });
            } catch (EmptyValue) {
                return undefined
            }

            return result;
        }


        showErrorOnButton(btn, msg) {
            $(btn).text(msg)
                .css('background-color', '#ee1700');
            setTimeout(function () {
                $(btn).text("Dalej")
                    .css('background-color', '#ffffff')
            }, 3000);
        }

        loadInstitution() {
            const container = $(this.slides[6]);
            container.find('div.form-group.form-group--checkbox').remove();
            $.getJSON('/add_donation', {
                step: 3,
                categories: this.selectedCategory(),
            }, function (data) {
                $(data).map(function (id, inst) {
                    container.find('h3').after($(`
                    <div class="form-group form-group--checkbox">
                        <label>
                            <input type="radio" name="organization" value="${inst[0]}"/>
                            <span class="checkbox radio"></span>
                            <span class="description">
                                  <div class="title">Fundacja “${inst[1]}"</div>
                                  <div class="subtitle">
                                    Cel i misja: ${inst[2]}.
                                  </div>
                                </span>
                        </label>
                    </div>                
                `))
                });
            })
        }

        showDonation() {
            this.receipt = this.checkReceiptForm();
            let container = $(this.slides[8]),
                category_list = "";
            $('input[name="categories"]:checked').map(function (id, value) {
                category_list += $(value).siblings('.description').text() + ','
            });
            console.log(this.receipt);
            container.find('ul').first().remove();
            container.find('h4').first().after($(`
                            <ul>
                                <li>
                                    <span class="icon icon-bag"></span>
                                    <span class="summary--text"
                                    >${this.amountOfBags()} worki z ${category_list}</span
                                    >
                                </li>

                                <li>
                                    <span class="icon icon-hand"></span>
                                    <span class="summary--text"
                                    >Dla "${$(this.selectedInstitution()).siblings('.description').find('.title').text()}"</span
                                    >
                                </li>
                            </ul>
                            <div class="form-section form-section--columns">
                                <div class="form-section--column">
                                    <h4>Adres odbioru:</h4>
                                    <ul>
                                        <li>${this.receipt.address}</li>
                                        <li>${this.receipt.city}</li>
                                        <li>${this.receipt.postcode}</li>
                                        <li>${this.receipt.phone}</li>
                                    </ul>
                                </div>

                                <div class="form-section--column">
                                    <h4>Termin odbioru:</h4>
                                    <ul>
                                        <li>${this.receipt.data}</li>
                                        <li>${this.receipt.time}</li>
                                        <li>${$('textarea').val()}</li>
                                    </ul>
                                </div>
                            </div>
                            

           `))

        }

        /**
         * Update form front-end
         * Show next or previous section etc.
         */
        updateForm() {
            this.$step.innerText = this.currentStep;

            if (this.currentStep === 2) {
                this.selectedCategories = this.selectedCategory()
                this.loadInstitution();
            } else if (this.currentStep === 5) {
                this.showDonation();
            }

            // TODO: Validation

            this.slides.forEach(slide => {
                slide.classList.remove("active");

                if (slide.dataset.step == this.currentStep) {
                    slide.classList.add("active");
                }

            });

            this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
            this.$step.parentElement.hidden = this.currentStep >= 6;

            // TODO: get data from inputs and show them in summary

        }

        /**
         * Submit form
         *
         * TODO: validation, send data to server
         */
        submit(e) {
            console.log("submite!")
            // e.preventDefault();
            // // this.currentStep++;
            // // this.updateForm();
            // console.log( $(this.$form).find(form))
            // $(this.$form).find(form).submit()
        }
    }

    const form = document.querySelector(".form--steps");
    if (form !== null) {
        new FormSteps(form);
    }
});
