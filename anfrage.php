<?php
/*
 * Formularversand erdel metallbau (Kontakt, Hörmann Tore/Türen, Kurzbewerbung) an info@erdel-metallbau.de.
 * Läuft auf dem IONOS-Webspace (PHP 8). Spamschutz: reCAPTCHA v3 (serverseitig geprüft), Honeypot,
 * Mindest-Ausfüllzeit, einfache Sperre je IP. Antwort immer JSON: {"ok":true} oder {"ok":false,"error":"…"}.
 * Zugangsdaten stehen in anfrage-config.php (NICHT im Repo, Vorlage: anfrage-config.example.php).
 */
declare(strict_types=1);
header('Content-Type: application/json; charset=utf-8');
header('X-Robots-Tag: noindex');

function antwort(bool $ok, string $fehler = '', int $code = 200): never {
    http_response_code($code);
    echo json_encode($ok ? ['ok' => true] : ['ok' => false, 'error' => $fehler], JSON_UNESCAPED_UNICODE);
    exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') antwort(false, 'Nur POST.', 405);
$cfgDatei = __DIR__ . '/anfrage-config.php';
if (!is_file($cfgDatei)) antwort(false, 'Der Versand ist noch nicht eingerichtet. Bitte rufen Sie uns an: 06195 63192.', 500);
$cfg = require $cfgDatei;

const FORMULARE = [
    'kontakt'   => 'Kontaktanfrage',
    'tore'      => 'Anfrage Hörmann-Tor',
    'tueren'    => 'Anfrage Hörmann-Tür',
    'bewerbung' => 'Kurzbewerbung',
];
const ENDUNGEN = ['jpg', 'jpeg', 'png', 'heic', 'webp', 'pdf'];
const MAX_DATEIEN = 10;
const MAX_BYTES = 15 * 1024 * 1024;   // gesamt, passt zu Exchange Online (25 MB nach Base64)

$feld = fn(string $k, int $max = 300): string => trim(mb_substr(str_replace("\0", '', (string)($_POST[$k] ?? '')), 0, $max));
$form = $feld('nxm_form', 20);
if (!isset(FORMULARE[$form])) antwort(false, 'Unbekanntes Formular.', 400);

// Honeypot und Mindestzeit (Bots füllen sofort alles aus)
if ($feld('website') !== '') antwort(true);
$start = (int)$feld('nxm_t', 20);
if ($start > 0 && (time() * 1000 - $start) < 3000) antwort(false, 'Bitte nehmen Sie sich einen Moment Zeit und senden Sie erneut.', 429);

// Sperre: höchstens 5 Anfragen je IP in 10 Minuten
$ip = $_SERVER['REMOTE_ADDR'] ?? '';
$sperre = sys_get_temp_dir() . '/nxm-anfrage-' . hash('sha256', $ip . ($cfg['secret'] ?? ''));
$zeiten = array_filter(is_file($sperre) ? (array)json_decode((string)file_get_contents($sperre), true) : [], fn($t) => $t > time() - 600);
if (count($zeiten) >= 5) antwort(false, 'Zu viele Anfragen in kurzer Zeit. Bitte versuchen Sie es später erneut oder rufen Sie uns an.', 429);

// reCAPTCHA v3
if (empty($cfg['test'])) {
    $token = $feld('nxm_token', 4000);
    if ($token === '') antwort(false, 'Der Spamschutz konnte nicht geladen werden. Bitte laden Sie die Seite neu.', 400);
    $ctx = stream_context_create(['http' => [
        'method' => 'POST', 'timeout' => 8,
        'header' => "Content-Type: application/x-www-form-urlencoded\r\n",
        'content' => http_build_query(['secret' => $cfg['secret'], 'response' => $token, 'remoteip' => $ip]),
    ]]);
    $r = json_decode((string)@file_get_contents('https://www.google.com/recaptcha/api/siteverify', false, $ctx), true);
    if (!is_array($r) || empty($r['success']) || ($r['action'] ?? '') !== 'anfrage' || ($r['score'] ?? 0) < ($cfg['min_score'] ?? 0.5)) {
        antwort(false, 'Ihre Anfrage wurde vom Spamschutz zurückgehalten. Bitte rufen Sie uns an: 06195 63192.', 400);
    }
}

// Pflichtfelder
$name = $feld('name-1', 120);
$mail = $feld('email-1', 200);
$tel = $feld('phone-1', 60);
$ort = $feld('name-5', 120);
$text = $feld('textarea-1', 5000);
$stelle = $feld('select-1', 120);
if ($name === '') antwort(false, 'Bitte geben Sie Ihren Namen an.', 400);
if ($mail !== '' && !filter_var($mail, FILTER_VALIDATE_EMAIL)) antwort(false, 'Bitte prüfen Sie Ihre E-Mail-Adresse.', 400);
if (in_array($form, ['kontakt', 'tore', 'tueren'], true) && $mail === '') antwort(false, 'Bitte geben Sie Ihre E-Mail-Adresse an.', 400);
if (in_array($form, ['tore', 'tueren', 'bewerbung'], true) && $tel === '') antwort(false, 'Bitte geben Sie Ihre Telefonnummer an.', 400);
if (in_array($form, ['tore', 'tueren'], true) && $ort === '') antwort(false, 'Bitte geben Sie PLZ und Ort an.', 400);
if ($feld('datenschutz', 10) === '') antwort(false, 'Bitte bestätigen Sie die Datenschutzerklärung.', 400);

// Anhänge
$anhaenge = [];
if (!empty($_FILES['upload-1']['name']) && is_array($_FILES['upload-1']['name'])) {
    $summe = 0;
    foreach ($_FILES['upload-1']['name'] as $i => $orig) {
        if (($_FILES['upload-1']['error'][$i] ?? UPLOAD_ERR_NO_FILE) === UPLOAD_ERR_NO_FILE) continue;
        if ($_FILES['upload-1']['error'][$i] !== UPLOAD_ERR_OK) antwort(false, 'Eine Datei konnte nicht hochgeladen werden.', 400);
        $tmp = $_FILES['upload-1']['tmp_name'][$i];
        $endung = strtolower(pathinfo((string)$orig, PATHINFO_EXTENSION));
        if (!in_array($endung, ENDUNGEN, true) || !is_uploaded_file($tmp)) antwort(false, 'Erlaubt sind JPG, PNG, HEIC, WEBP und PDF.', 400);
        $summe += filesize($tmp);
        if (count($anhaenge) >= MAX_DATEIEN || $summe > MAX_BYTES) antwort(false, 'Bitte höchstens 10 Dateien und zusammen 15 MB senden.', 400);
        $sauber = preg_replace('/[^A-Za-z0-9._-]+/', '_', pathinfo((string)$orig, PATHINFO_FILENAME)) ?: 'datei';
        $anhaenge[] = ['name' => mb_substr($sauber, 0, 60) . '.' . $endung, 'daten' => file_get_contents($tmp)];
    }
}

// E-Mail
$zeilen = [
    'Formular' => FORMULARE[$form],
    'Name' => $name, 'E-Mail' => $mail, 'Telefon' => $tel, 'PLZ und Ort' => $ort, 'Stelle' => $stelle,
];
$body = FORMULARE[$form] . " über erdel-metallbau.de\n\n";
foreach ($zeilen as $k => $v) if ($v !== '' && $k !== 'Formular') $body .= str_pad($k . ':', 14) . $v . "\n";
if ($text !== '') $body .= "\nNachricht:\n" . $text . "\n";
if ($anhaenge) $body .= "\nAnhänge: " . count($anhaenge) . "\n";
$body .= "\nDatenschutz-Einwilligung: erteilt am " . date('d.m.Y \u\m H:i') . " Uhr\n";

$enc = fn(string $s): string => '=?UTF-8?B?' . base64_encode($s) . '?=';
$betreff = FORMULARE[$form] . ': ' . preg_replace('/[\r\n]+/', ' ', $name);
$von = $cfg['from'] ?? 'website@erdel-metallbau.de';
$header = [
    'From: ' . $enc('Website erdel metallbau') . ' <' . $von . '>',
    'MIME-Version: 1.0',
];
if ($mail !== '') $header[] = 'Reply-To: ' . $enc(preg_replace('/[\r\n]+/', ' ', $name)) . ' <' . $mail . '>';

if ($anhaenge) {
    $grenze = 'nxm-' . bin2hex(random_bytes(12));
    $header[] = 'Content-Type: multipart/mixed; boundary="' . $grenze . '"';
    $inhalt = "--$grenze\r\nContent-Type: text/plain; charset=UTF-8\r\nContent-Transfer-Encoding: base64\r\n\r\n"
        . chunk_split(base64_encode($body)) . "\r\n";
    foreach ($anhaenge as $a) {
        $inhalt .= "--$grenze\r\nContent-Type: application/octet-stream; name=\"{$a['name']}\"\r\n"
            . "Content-Transfer-Encoding: base64\r\nContent-Disposition: attachment; filename=\"{$a['name']}\"\r\n\r\n"
            . chunk_split(base64_encode($a['daten'])) . "\r\n";
    }
    $inhalt .= "--$grenze--";
} else {
    $header[] = 'Content-Type: text/plain; charset=UTF-8';
    $header[] = 'Content-Transfer-Encoding: base64';
    $inhalt = chunk_split(base64_encode($body));
}

if (!empty($cfg['test'])) {
    // Testbetrieb: Mail als Datei ablegen statt senden
    file_put_contents(sys_get_temp_dir() . '/nxm-anfrage-test.eml', "To: {$cfg['to']}\r\nSubject: " . $enc($betreff) . "\r\n" . implode("\r\n", $header) . "\r\n\r\n" . $inhalt);
    $ok = true;
} else {
    $ok = mail($cfg['to'] ?? 'info@erdel-metallbau.de', $enc($betreff), $inhalt, implode("\r\n", $header), '-f' . $von);
}
if (!$ok) antwort(false, 'Der Versand hat leider nicht geklappt. Bitte rufen Sie uns an: 06195 63192.', 500);

$zeiten[] = time();
@file_put_contents($sperre, json_encode(array_values($zeiten)));
antwort(true);
