function goToHomePage() {
    localStorage.setItem('liked_books', JSON.stringify(liked_books));
    window.location.href = "/";
}

var liked_books = JSON.parse(localStorage.getItem('liked_books'));

document.addEventListener('DOMContentLoaded', function() {
    removeButton = document.getElementById("removeButton")

    removeButton.addEventListener('click', function() {
        // Refresh the page
        localStorage.clear();
        location.reload();
    });

    UserList = document.getElementById('user-list');

    for (var i = 0; i < liked_books.length; i++) {
        bookVal = document.createElement("li");
        bookVal.innerHTML = liked_books[i];
        UserList.appendChild(bookVal);
    }

    recsButton = document.getElementById("getsRecsButton")

    recsButton.addEventListener('click', function() {
        showLoadingSpinner()
        const books = liked_books.map(item => {
            const match = item.match(/\d+/);
            return match ? match[0] : null;
        });

        fetch('/perform-recs', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ selectedBooks: books })
        })
        .then(response => response.json())
        .then(data => {
            hideLoadingSpinner()

            RecsList = document.getElementById('rec-list');
            
            for (var i = 1; i < data.length; i++) {
                bookVal = document.createElement("li");
                bookVal.innerHTML = data[i];
                RecsList.appendChild(bookVal);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
})

function showLoadingSpinner() {
    document.getElementById("loading-spinner").style.display = "block";
  }
  
// Function to hide the loading spinner
function hideLoadingSpinner() {
    document.getElementById("loading-spinner").style.display = "none";
}
