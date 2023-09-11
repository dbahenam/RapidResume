// document.addEventListener("DOMContentLoaded", function() {
//     const textarea = document.querySelector('textarea');

//     textarea.addEventListener('keydown', function(e) {
//         if (e.key === 'Enter') {
//             setTimeout(() => {
//                 const value = textarea.value;
//                 if (!value.endsWith('• ')) {
//                     textarea.value += '• ';
//                 }
//             }, 0);
//         }
//     });

//     textarea.addEventListener('focus', function() {
//         if (!textarea.value.trim()) {
//             textarea.value = '• ';
//         }
//     });

// });