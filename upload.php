<?php
$target_dir = "uploads/";
$botDirectory = $_POST['botname'];
$target_file = $target_dir . $botDirectory. "/" .basename($_FILES["fileToUpload"]["name"]);
$uploadOk = 1;
$FileType = pathinfo($target_file,PATHINFO_EXTENSION);

//Check if the bot's folder exists
if (!file_exists('uploads/'. $botDirectory)) {
    mkdir('uploads/'. $botDirectory, 0777, true);
    $uploadOk = 1;
}


// Check if file already exists, rename it
if (file_exists($target_file)) {
    $target_file = $target_file . '(1)';
    $uploadOk = 1;
}

// Check if $uploadOk is set to 0 by an error
if ($uploadOk == 0) {
    header('Upl0ad3d: False');
// if everything is ok, try to upload file
} else {
    if (move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $target_file)) {
        header('Upl0ad3d: True');
        $checksum = md5_file($target_file);
        header('checksum: '. $checksum);
    } else {
        header('Upl0ad3d: False');
    }
}
?>
