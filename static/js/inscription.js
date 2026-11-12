// static/js/inscription.js - JS séparé du HTML, norme industrie
// On gère le drag & drop ici, pas dans le HTML

const dropzone = document.getElementById('dropzone'); // document.getElementById = retrouve l'élément HTML avec id="dropzone"
const fileInput = document.getElementById('fileInput'); // Retrouve l'input file caché

dropzone.addEventListener('click', () => fileInput.click()); // addEventListener('click') = quand on clique sur la zone, on ouvre le sélecteur de fichier

// Quand on survole la zone avec un fichier, on la met en vert
dropzone.addEventListener('dragover', (e) => { // e = événement
  e.preventDefault(); // preventDefault = empêche le navigateur d'ouvrir le fichier
  dropzone.style.borderColor = 'green'; // On change la bordure en vert
});

// Quand on dépose le fichier
dropzone.addEventListener('drop', (e) => {
  e.preventDefault(); // Empêche l'ouverture
  dropzone.textContent = `✅ ${e.dataTransfer.files.length} fichier(s) déposé(s) - En vrai, on l'enverra avec le formulaire`; // dataTransfer.files = fichiers déposés. On affiche combien
});