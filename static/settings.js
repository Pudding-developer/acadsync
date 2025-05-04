function toggleDropdown() {
    const dropdownButton = document.querySelector('.settings-header-button');
    const dropdownContent = dropdownButton.nextElementSibling; // Get the dropdown content
    dropdownContent.classList.toggle('active'); // Toggle the active class
}