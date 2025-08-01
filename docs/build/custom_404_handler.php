<?php
// Get the preferred language from the browser
$acceptLang = $_SERVER['HTTP_ACCEPT_LANGUAGE'] ?? '';
$lang = 'en'; // default

if (stripos($acceptLang, 'fr') === 0) {
    $lang = 'fr';
}

// Redirect to language-specific 404 page
header("Location: /$lang/404.html", true, 302);
exit;