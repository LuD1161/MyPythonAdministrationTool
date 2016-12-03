//For Communication with bot using a text file on my website
<?php
if ($_GET['g']=='data'){
	if(filesize("comm.txt")>0){
		$myFile = fopen("comm.txt","r");
		echo (fread($myFile, filesize("comm.txt")));
    	fclose($myFile);
	}
	else echo "Empty";
}
else{
	$myFile = fopen("comm.txt","w");
	$temp = '';

	if(isset($_GET['p'])){
		$temp = $_GET['p'];
		fwrite($myFile, $temp);
		header('Upl0ad3d: True');
	}
	else if(isset($_POST['p'])){
		$temp = $_POST['p'];
		fwrite($myFile, $temp);
		header('Upl0ad3d: True');
	}
	fclose($myFile);
}
?>
