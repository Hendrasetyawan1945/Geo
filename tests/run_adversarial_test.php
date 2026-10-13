<?php

declare(strict_types=1);

require_once __DIR__ . '/../vendor/autoload.php';
require_once __DIR__ . '/../vendor/codeigniter4/framework/system/Test/bootstrap.php';
require_once __DIR__ . '/unit/AdversarialLinguisticValidationTest.php';

use Tests\Unit\AdversarialLinguisticValidationTest;

$test = new AdversarialLinguisticValidationTest();

$methods = get_class_methods($test);
$testMethods = array_filter($methods, fn($m) => str_starts_with($m, 'test'));

echo "================================================================================\n";
echo "  PENGUJIAN VALIDASI ADVERSARIAL, LINGUISTIK MINANG, & GROUNDING KETAT\n";
echo "================================================================================\n";

$passed = 0;
$total = count($testMethods);

foreach ($testMethods as $method) {
    try {
        // Panggil setUp sebelum setiap method
        $setUpMethod = new ReflectionMethod($test, 'setUp');
        $setUpMethod->setAccessible(true);
        $setUpMethod->invoke($test);

        $test->$method();
        echo "  [PASS] {$method}\n";
        $passed++;
    } catch (\Throwable $e) {
        echo "  [FAIL] {$method}: " . $e->getMessage() . " (Line " . $e->getLine() . ")\n";
    }
}

echo "--------------------------------------------------------------------------------\n";
echo "Hasil: {$passed}/{$total} Pengujian Lulus (" . number_format(($passed / $total) * 100, 2) . "%)\n";
echo "================================================================================\n";
