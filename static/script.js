document.querySelectorAll('.film').forEach((button) => {
    button.addEventListener('click', () => {
        fetch(`/search/${button.id}`, {
            method: 'POST',
            body: JSON.stringify({"title": button.id}),
        })
        .then(response => {
            if (response.ok) {
                window.location.href = `/search/${button.id}`;
            } else {
                console.error('Error:', response.statusText);
            }
        })
        .catch(error => {
            console.error('Fetch error:', error);
        });
    });
});
