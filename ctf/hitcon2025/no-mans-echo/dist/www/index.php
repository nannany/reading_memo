<?php
	$probe = (int)@$_GET['probe'];
	$range = range($probe, $probe + 42);
	shuffle($range);

	foreach ($range as $k => $port) {
		$target = sprintf("tcp://%s:%d", $_SERVER['SERVER_ADDR'], $port);
		$fp = @stream_socket_client($target, $errno, $errstr, 1);
	    if (!$fp) continue;

	    stream_set_timeout($fp, 1);
	    fwrite($fp, file_get_contents("php://input"));
	    $data = fgets($fp);
	    if (strlen($data) > 0) {
	    	$data = json_decode($data);
	    	if (isset($data->signal) && $data->signal == 'Arrival')
	    		eval($data->logogram);
	    	
	    	fclose($fp);
	    	exit(-1);
	    }
	} 
	highlight_file(__FILE__);