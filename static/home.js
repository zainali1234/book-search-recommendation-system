liked_books = 0;
if (!(liked_books = JSON.parse(localStorage.getItem('liked_books')))) {
  console.log("Starting new storage...")
  liked_books = []
}

// Wait for the DOM to load
document.addEventListener('DOMContentLoaded', function() {
    // Get the input and button elements
    const searchInput = document.getElementById('searchInput');
    const submitButton = document.getElementById('submitButton');
  
    // Add an event listener to the button's click event
    if (submitButton) {
      submitButton.addEventListener('click', function() {
        // Get the value entered in the search input
        const searchTerm = searchInput.value;
          if (searchTerm) {
            // Make an AJAX request to the Flask route to call the Python function
            showLoadingSpinner()
            fetch('/perform-search', {
                method: 'POST',
                headers: {
                'Content-Type': 'application/json'
                },
                body: JSON.stringify({ searchTerm: searchTerm })
            })
            .then(response => response.json())
            .then(data => {
                // console.log(data);
                hideLoadingSpinner()
                removeElementsAfterCreation()
                addValuesToDOM(data)
            })
            .catch(error => {
                console.error('Error:', error);
            });
          }
      });
    }
  });

// Function to add values to the list
function addValuesToDOM(values) {
  const list = document.getElementById("list");

  // Iterate over the array of values
  values.forEach((value) => {
    // Create a new list item
    const listItem = document.createElement("li");
    listItem.setAttribute('id', value[1]);

    const btn = document.createElement('button');
    btn.setAttribute('id', value[0]);
    btn.classList.add('button-custom');
    btn.innerHTML = '+'

    btn.addEventListener("click", function() {
      // Actions to perform when the button is pressed
      if (liked_books) {
        if (liked_books.includes(this.id + " " + (btn.parentNode).id)) {
          console.log("Book already added")
        }
        else {
          liked_books.push(this.id + " " + (btn.parentNode).id)
          console.log(liked_books)
        }
      }
    });

    listItem.appendChild(btn);

    const link = document.createElement("a");
    link.setAttribute("href", value[3]);

    link.innerHTML = truncateString(value[1]) + " " + value[0];
    link.style.fontStyle = "italic";

    listItem.appendChild(link);

    const img = document.createElement("img");
    img.setAttribute("src", value[4]);

    img.style.float = 'right';
    img.style.marginLeft = 'auto';

    // Append the list item to the list
    listItem.appendChild(img)
    
    list.appendChild(listItem);
    // Trigger the animation
    setTimeout(() => {
      listItem.style.opacity = "1";
      listItem.style.transform = "translateY(0)";
    }, 100);
  });
}

function removeElementsAfterCreation() {
    const list = document.getElementById("list");
  
    // Remove all child elements of the list
    while (list.firstChild) {
      list.firstChild.remove();
    }
}

function truncateString(str) {
  if (str.length > 55) {
    return str.slice(0, 55) + "...";
  }
  return str;
}

function goToListPage() {
  localStorage.setItem('liked_books', JSON.stringify(liked_books));
  window.location.href = "/mylist";
}

function showLoadingSpinner() {
  document.getElementById("loading-spinner").style.display = "block";
}

// Function to hide the loading spinner
function hideLoadingSpinner() {
  document.getElementById("loading-spinner").style.display = "none";
}