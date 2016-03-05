<?php

# Setting time and memory limits
ini_set('max_execution_time',0);
ini_set('memory_limit', '128M');

require_once 'PHPExcel.php';
require_once 'PHPExcel/IOFactory.php';
require_once 'RollingCurl.class.php';
require_once 'AngryCurl.class.php';

$AC = new AngryCurl('callback_function');

$objPHPExcel = new PHPExcel();
$objPHPExcel->setActiveSheetIndex(0);

$url = 'https://www.vfbank.ru/garant/calcdo';
$fz = "1";
$program = "2";
$avans = "0";
$time_array = array("30", "60", "90", "120", "150", "180", "210", "240", "270", "300", "330", "360", "390", "420", "450", "480", "510", "540", "570", "600", "630", "660", "690", "720", "760");
$amount_array = array("100000", "200000", "300000", "400000", "500000", "600000", "700000", "800000", "900000", "1000000", "1100000", "1200000", "1300000", "1400000", "1500000", "1600000", "1700000", "1800000", "1900000", "2000000", "2100000", "2200000", "2300000", "2400000", "2500000", "2600000", "2700000", "2800000", "2900000", "3000000", "3100000", "3200000", "3300000", "3400000", "3500000", "3600000", "3700000", "3800000", "3900000", "4000000", "4100000", "4200000", "4300000", "4400000", "4500000", "4600000", "4700000", "4800000", "4900000", "5000000", "5100000", "5200000", "5300000", "5400000", "5500000", "5600000", "5700000", "5800000", "5900000");

/* Set header */
$objPHPExcel->getActiveSheet()->setCellValueByColumnAndRow(0, 1, 'сумма');
set_header_style(0, 1);
set_leftside_style(0, 1);

$row = 1;
$col = 1;
foreach ($time_array as $time) {
    $objPHPExcel->getActiveSheet()->setCellValueByColumnAndRow($col, $row, $time);
    set_header_style($col, $row);
    $col += 1;
}

/* Set left side */
$row = 2;
$col = 0;
foreach ($amount_array as $amount) {
    $objPHPExcel->getActiveSheet()->setCellValueByColumnAndRow($col, $row, $amount);
    set_leftside_style($col, $row);
    $row += 1;
}

/* Populate commision table */
$row = 2;
foreach ($amount_array as $amount) {
    $col = 1;
    foreach ($time_array as $time) {
        /* Multiple thread implementation */
        $options = array();
        $options['fz'] = $fz;
        $options['program'] = $program;
        $options['avans'] = $avans;
        $options['money'] = $amount;
        $options['dd'] = $time;
        $AC->post($url, $options);
        $col += 1;
    }
    $row += 1;
}

$AC->execute(5);

# Destroying
unset($AC);

$objWriter = PHPExcel_IOFactory::createWriter($objPHPExcel, 'Excel2007');
$objWriter->save(str_replace('.php', '.xls', __FILE__));

# Callback function example
function callback_function($response, $info, $request)
{
    global $objPHPExcel, $time_array, $amount_array;
    
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
        
        preg_match("/Значение комиссии: (.*?)</", $response, $m);
        $commision = str_replace(' Руб.','',$m[1]);
        $row = array_search($request->post_data['money'], $amount_array)+2;
        $col = array_search($request->post_data['dd'], $time_array)+1;
        $objPHPExcel->getActiveSheet()->setCellValueByColumnAndRow($col, $row, $commision);
        set_commision_style($col, $row);
    }
    
    return;
}

function set_header_style($x,$y){
    global $objPHPExcel;
    $cell_name = coordinates($x,$y);
    $objPHPExcel->getActiveSheet()->getStyle($cell_name)->getFont()->setBold(true);
    $objPHPExcel->getActiveSheet()->getStyle($cell_name)->getFill()->setFillType(PHPExcel_Style_Fill::FILL_SOLID)->getStartColor()->setARGB('FF99CCFF');
    $objPHPExcel->getActiveSheet()->getStyle($cell_name)->getBorders()->getBottom()->setBorderStyle(PHPExcel_Style_Border::BORDER_THIN);
}

function set_leftside_style($x,$y){
    global $objPHPExcel;
    $cell_name = coordinates($x,$y);
    $objPHPExcel->getActiveSheet()->getStyle($cell_name)->getBorders()->getRight()->setBorderStyle(PHPExcel_Style_Border::BORDER_THIN);
}

function set_commision_style($x,$y){
    global $objPHPExcel;
    $cell_name = coordinates($x,$y);
    $objPHPExcel->getActiveSheet()->getStyle($cell_name)->getFill()->setFillType(PHPExcel_Style_Fill::FILL_SOLID)->getStartColor()->setARGB('FFFFFF00');
}

/*
 * $x - column
 * $y - row
 */
function coordinates($x,$y){
    return PHPExcel_Cell::stringFromColumnIndex($x).$y;
}
