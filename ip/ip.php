<?php

	if (!empty($_SERVER['HTTP_CLIENT_IP'])){
		$ip = $_SERVER['HTTP_CLIENT_IP'] . "\r\n";
	}

	elseif(!empty($_SERVER['HTTP_X_FORWARDED_FOR'])){
		$ip = $_SERVER['HTTP_X_FORWARDED_FOR'] . "\r\n";
	}

	else{
		$ip = $_SERVER['REMOTE_ADDR'] ."\r\n";
	}

$user_agent = $_SERVER['HTTP_USER_AGENT'] . "\r\n\r\n";

$file_save = fopen("ip.txt", "a");

$ip_text = "IP: ";
$user_agent_text = "|_____ User-Agent : ";

fwrite($file_save, $ip_text);
fwrite($file_save, $ip);
fwrite($file_save, $user_agent_text);
fwrite($file_save, $user_agent);

fclose($file_save);

$file = fopen("ip_addr.txt", "a");

$ip_text = "IP: ";
$user_agent_text = "|_____ User-Agent : ";

fwrite($file, $ip_text);
fwrite($file, $ip);
fwrite($file, $user_agent_text);
fwrite($file, $user_agent);

fclose($file);

?>