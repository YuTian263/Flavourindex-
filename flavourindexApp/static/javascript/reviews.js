const stars = document.querySelectorAll('.star');
const input = document.getElementById('rating-input');
stars.forEach(star => {
    star.addEventListener('click', () => {
        const val = parseInt(star.dataset.val);
        input.value = val;
        stars.forEach(s => s.style.color = parseInt(s.dataset.val) <= val ? '#f5a623' : '#ccc');
    });
    star.addEventListener('mouseover', () => {
        const val = parseInt(star.dataset.val);
        stars.forEach(s => s.style.color = parseInt(s.dataset.val) <= val ? '#f5a623' : '#ccc');
    });
});
document.getElementById('stars').addEventListener('mouseleave', () => {
    const val = parseInt(input.value) || 0;
    stars.forEach(s => s.style.color = parseInt(s.dataset.val) <= val ? '#f5a623' : '#ccc');
});