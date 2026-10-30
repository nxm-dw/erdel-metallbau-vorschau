<?php
// Vorlage: als anfrage-config.php neben anfrage.php auf den IONOS-Webspace legen (nie ins Repo).
return [
    'secret'    => 'GEHEIMER-RECAPTCHA-SCHLUESSEL',   // reCAPTCHA v3, „Geheimer Schlüssel“
    'to'        => 'info@erdel-metallbau.de',
    'from'      => 'website@erdel-metallbau.de',      // Absender; SPF muss IONOS erlauben (siehe README)
    'min_score' => 0.5,
    'test'      => false,                             // true = kein reCAPTCHA, Mail landet als Datei im Temp-Ordner
];
