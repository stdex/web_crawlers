<?php

# Setting time and memory limits
ini_set('max_execution_time',0);
ini_set('memory_limit', '128M');

define('AC_DIR', dirname(__FILE__));

# Including classes
require_once( AC_DIR . DIRECTORY_SEPARATOR . 'classes' . DIRECTORY_SEPARATOR . 'RollingCurl.class.php');
require_once( AC_DIR . DIRECTORY_SEPARATOR . 'classes' . DIRECTORY_SEPARATOR . 'AngryCurl.class.php');

# Initializing AngryCurl instance with callback function named 'callback_function'
$AC = new AngryCurl('callback_function');

# Initializing so called 'web-console mode' with direct cosnole-like output
$AC->init_console();

$filexml = 'sitemap.xml';
$urls = array();
if (file_exists($filexml)) {
    $sitemap = simplexml_load_file($filexml);
    foreach ($sitemap as $url) {
        $urls[] = $url->loc;
    }
}

# Basic request usage (for extended - see demo folder)
foreach ($urls as $url) {
    $AC->get($url);
}

# Starting with number of threads = 3
$AC->execute(2);

# You may pring debug information, if console_mode is NOT on ( $AC->init_console(); )
//AngryCurl::print_debug(); 

# Destroying
unset($AC);

# Callback function example
function callback_function($response, $info, $request)
{
    if($info['http_code']!==200)
    {
        AngryCurl::add_debug_msg(
            "->\t" .
            $request->options[CURLOPT_PROXY] .
            "\tFAILED\t" .
            $info['http_code'] .
            "\t" .
            $info['total_time'] .
            "\t" .
            $info['url']
        );
    }else
    {
        AngryCurl::add_debug_msg(
            "->\t" .
            $request->options[CURLOPT_PROXY] .
            "\tOK\t" .
            $info['http_code'] .
            "\t" .
            $info['total_time'] .
            "\t" .
            $info['url']
        );
        
        preg_match("/html;/",$info['content_type'],$find_content_type);
        
        if(isset($find_content_type[0])) {
            
            $doc = new DOMDocument();
            $doc->loadHTML($response);
            
            $metas = $doc->getElementsByTagName('meta');

            $description = "";
            foreach ($metas as $meta) {
                if (strtolower($meta->getAttribute('name')) == 'description') {
                    $content = $meta->getAttribute('content');
                    $description = iconv("UTF-8", "windows-1251", $content);
                }
            }
            $fp = fopen("output_sitemap.csv", 'a');
            $turl = iconv("UTF-8", "windows-1251", $info['url']);
            fputcsv($fp, array($turl,$description), ';');
            fclose($fp);
        }
        
    }
    
    return;
}
