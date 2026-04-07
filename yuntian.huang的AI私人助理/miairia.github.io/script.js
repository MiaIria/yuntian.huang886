document.addEventListener('DOMContentLoaded', () => {
    // 1. Typewriter Effect
    const text = "你好，这里是黄运添的私人频道";
    const typeWriterElement = document.getElementById('typewriter');
    typeWriterElement.textContent = '';
    
    let i = 0;
    const speed = 100; // ms per char
    
    function typeWriter() {
        if (i < text.length) {
            typeWriterElement.textContent += text.charAt(i);
            i++;
            setTimeout(typeWriter, speed);
        } else {
            // Typing finished, maybe add a slight pause then keep cursor blinking
            document.querySelector('.cursor').style.animation = 'blink 1s step-end infinite';
        }
    }
    
    // Start typing after a short delay
    setTimeout(typeWriter, 500);

    // 2. Scroll Animation (Intersection Observer)
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.15
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                
                // Trigger cascading animations if element has children with cascade-anim
                const cascadeChildren = entry.target.querySelectorAll('.cascade-anim');
                if (cascadeChildren.length > 0) {
                    cascadeChildren.forEach((child, index) => {
                        setTimeout(() => {
                            child.style.opacity = '1';
                            child.style.transform = 'translateY(0)';
                        }, index * 150);
                    });
                }
                
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Initial setup for cascade animations
    document.querySelectorAll('.cascade-anim').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s ease-out, transform 0.6s ease-out';
    });

    // Observe all sections and fade-in elements
    document.querySelectorAll('.fade-in, .section').forEach(el => {
        observer.observe(el);
    });

    // 3. Smooth Scrolling for Navigation Links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                const headerOffset = 70; // Height of nav bar
                const elementPosition = targetElement.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
  
                window.scrollTo({
                    top: offsetPosition,
                    behavior: "smooth"
                });
            }
        });
    });

    // 4. Parallax effect on mouse move for background gradients
    const bg1 = document.querySelector('.bg-grad-1');
    const bg2 = document.querySelector('.bg-grad-2');
    
    document.addEventListener('mousemove', (e) => {
        const x = e.clientX / window.innerWidth;
        const y = e.clientY / window.innerHeight;
        
        bg1.style.transform = `translate(${x * 30}px, ${y * 30}px)`;
        bg2.style.transform = `translate(${x * -40}px, ${y * -40}px)`;
    });
});
