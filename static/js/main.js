document.addEventListener("DOMContentLoaded", function () {
    const fadeInElements = document.querySelectorAll('.fade-in');
    fadeInElements.forEach(element => {
        element.classList.add('visible');
    });

    const themeToggle = document.getElementById('themeToggle');
    function setTheme(mode) {
        if (mode === 'dark') {
            document.body.classList.add('dark-mode');
            themeToggle.textContent = '☀️ Light Mode';
            localStorage.setItem('theme', 'dark');
        } else {
            document.body.classList.remove('dark-mode');
            themeToggle.textContent = '🌙 Dark Mode';
            localStorage.setItem('theme', 'light');
        }
    }
    themeToggle.addEventListener('click', () => {
        if (document.body.classList.contains('dark-mode')) {
            setTheme('light');
        } else {
            setTheme('dark');
        }
    });
    const savedTheme = localStorage.getItem('theme') || 'light';
    setTheme(savedTheme);

    document.querySelectorAll('.animated-button').forEach(button => {
        button.addEventListener('click', () => {
            if (button.dataset.copy) {
                copyToClipboard(button.dataset.copy);
                button.textContent = 'Copied!';
                setTimeout(() => {
                    button.textContent = button.dataset.text;
                }, 2000);
            }
        });

        button.addEventListener('mouseover', () => {
            button.classList.add('hovered');
        });

        button.addEventListener('mouseout', () => {
            button.classList.remove('hovered');
        });
    });

    function copyToClipboard(text) {
        navigator.clipboard.writeText(text).then(function () {
            showFlashMessage('Copied: ' + text);
        }, function (err) {
            console.error('Copy error: ', err);
        });
    }

    function showFlashMessage(message) {
        const flashMessageDiv = document.getElementById('flash-message');
        flashMessageDiv.textContent = message;
        flashMessageDiv.classList.add('show');
        setTimeout(() => {
            flashMessageDiv.classList.remove('show');
        }, 3000);
    }

    const textBlocks = document.querySelectorAll('.text-block');

    textBlocks.forEach(block => {
        block.addEventListener('click', () => {
            const isFullContent = block.classList.contains('full-content');
            textBlocks.forEach(b => b.classList.remove('full-content'));
            if (!isFullContent) {
                block.classList.add('full-content');
            }
        });
    });

    document.addEventListener('click', (event) => {
        if (!event.target.closest('.text-block.full-content')) {
            textBlocks.forEach(block => {
                block.classList.remove('full-content');
            });
        }
    });

    // Add animation on scroll
    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, { threshold: 0.1 });

    fadeInElements.forEach(element => {
        observer.observe(element);
    });

    // Smooth scroll to top button
    const backToTopButton = document.getElementById('back-to-top');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 300) {
            backToTopButton.classList.add('show');
        } else {
            backToTopButton.classList.remove('show');
        }
    });

    backToTopButton.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });

    // Smooth scroll for internal links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Modal popups
    const modalTriggers = document.querySelectorAll('[data-modal]');
    const modalCloseButtons = document.querySelectorAll('.modal-close');

    modalTriggers.forEach(trigger => {
        trigger.addEventListener('click', function () {
            const modal = document.querySelector(this.dataset.modal);
            modal.classList.add('is-active');
        });
    });

    modalCloseButtons.forEach(button => {
        button.addEventListener('click', function () {
            this.closest('.modal').classList.remove('is-active');
        });
    });

    // Tooltips
    const tooltipElements = document.querySelectorAll('[data-tooltip]');
    tooltipElements.forEach(element => {
        element.addEventListener('mouseover', function () {
            const tooltip = document.createElement('div');
            tooltip.className = 'tooltip';
            tooltip.textContent = this.dataset.tooltip;
            document.body.appendChild(tooltip);
            const rect = this.getBoundingClientRect();
            tooltip.style.left = `${rect.left + window.scrollX + rect.width / 2 - tooltip.offsetWidth / 2}px`;
            tooltip.style.top = `${rect.top + window.scrollY - tooltip.offsetHeight - 10}px`;
        });

        element.addEventListener('mouseout', function () {
            document.querySelector('.tooltip').remove();
        });
    });

    // Image carousel
    const carousels = document.querySelectorAll('.carousel');
    carousels.forEach(carousel => {
        const slides = carousel.querySelectorAll('.carousel-slide');
        let currentIndex = 0;

        function showSlide(index) {
            slides.forEach((slide, i) => {
                slide.style.display = i === index ? 'block' : 'none';
            });
        }

        carousel.querySelector('.carousel-next').addEventListener('click', () => {
            currentIndex = (currentIndex + 1) % slides.length;
            showSlide(currentIndex);
        });

        carousel.querySelector('.carousel-prev').addEventListener('click', () => {
            currentIndex = (currentIndex - 1 + slides.length) % slides.length;
            showSlide(currentIndex);
        });

        showSlide(currentIndex);
    });
});