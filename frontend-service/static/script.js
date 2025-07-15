document.addEventListener('DOMContentLoaded', () => {

    // --- 1. Terminal Typing Animation ---
    const terminal = document.getElementById('terminal-content');
    const lines = [
        { text: 'himanshu-portfolio % gcloud run deploy frontend-service --platform=managed', speed: 50 },
        { text: 'Deploying service [frontend-service] to project [himanshu-tiwary-portfolio]...', speed: 20, delay: 500 },
        { text: '✓ Uploading sources...', speed: 20, isSuccess: true },
        { text: '✓ Building container...', speed: 20, isSuccess: true },
        { text: '✓ Creating new revision...', speed: 20, isSuccess: true },
        { text: '✓ Routing traffic...', speed: 20, isSuccess: true },
        { text: 'Done. Deployed service [frontend-service] to: ' , speed: 20, delay: 200},
        { text: 'https://frontend-service-xxxxxxxx-uc.a.run.app', speed: 50, isLink: true },
        { text: ' ', speed: 1, delay: 500 },
        { text: 'himanshu-portfolio % Welcome to my portfolio!', speed: 50}
    ];

    let lineIndex = 0;
    let timeout = 100;

    function typeLine() {
        if (lineIndex >= lines.length) {
            terminal.innerHTML += '<span class="cursor"></span>';
            return;
        }

        const currentLine = lines[lineIndex];
        const p = document.createElement('p');
        
        if (currentLine.isSuccess) {
            p.innerHTML = '<span class="text-success">✓</span> ';
        } else {
            p.innerHTML = '<span class="prompt">></span> ';
        }
        
        terminal.appendChild(p);

        let charIndex = 0;
        function typeChar() {
            if (charIndex < currentLine.text.length) {
                if (currentLine.isLink) {
                    p.innerHTML = `<span class="prompt">></span> <a href="#" class="terminal-link">${currentLine.text}</a>`;
                    charIndex = currentLine.text.length; // Skip typing for link
                } else {
                    p.innerHTML += currentLine.text.charAt(charIndex);
                }
                charIndex++;
                setTimeout(typeChar, currentLine.speed);
            } else {
                lineIndex++;
                timeout = currentLine.delay || 100;
                setTimeout(typeLine, timeout);
            }
        }
        typeChar();
    }
    
    typeLine();


    // --- 2. Fade-in on Scroll Animation ---
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target); // Animate only once
            }
        });
    }, { threshold: 0.1 }); // Trigger when 10% of the element is visible

    const elementsToAnimate = document.querySelectorAll('.fade-in');
    elementsToAnimate.forEach(el => observer.observe(el));

});
