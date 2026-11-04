<?php
namespace App\Http\Controllers;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;
class HelloController extends Controller
{
/**
 * GET /api/hello
 * GET /api/hello?name=Ana
 */
public function index(Request $request): JsonResponse
 {
// Leemos el parámetro "name" de la query string (o cadena vacía si no viene)
$name = trim((string) $request->query('name', ''));
$message = $name === ''
? 'Hello World'
: "Hello World {$name}";
return response()->json([
'message' => $message,
 ]);
 }
}
