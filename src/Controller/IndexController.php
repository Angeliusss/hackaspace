<?php

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;

class IndexController extends AbstractController
{
    #[Route('/', name: 'app_index')]
    public function index(): Response
    {

        // ====================================================================
        //
        // Path to the JSON files to compare
        $jsonFileA = '../public/dossier_fichiers_A/221410_A.json';
        $jsonFileB = '../public/dossier_fichiers_B/221410_B.json';

        // ====================================================================

        // Get the files contents
        $jsonStringFileA = file_get_contents($jsonFileA);
        $jsonStringFileB = file_get_contents($jsonFileB);

        // ====================================================================

        // Convert the JSON string to a PHP object, to display
        $dataFileA = json_decode($jsonStringFileA, true);
        $dataFileB = json_decode($jsonStringFileB, true);

        // ====================================================================

        // Create an array to hold the counts of key-value pairs for each object
        $dictCountsFileA = [];
        $dictCountsFileB = [];

        // ====================================================================
        
        $redshiftComparisonResults = [];

        foreach ($dataFileA as $index => $itemA) {
            $itemB = $dataFileB[$index] ?? null;
            
            if (!isset($itemA['Redshift']) || !isset($itemB['Redshift'])) {
                $redshiftComparisonResults[] = [
                    'index' => $index,
                    'message' => "La clé Redshift de l'objet {$index} n'existe pas dans le fichier A ou B. Comparaison impossible"
                ];
            } elseif ($itemA['Redshift'] !== $itemB['Redshift']) {
                $redshiftComparisonResults[] = [
                    'index' => $index,
                    'message' => "La clé 'Redshift' de l'objet {$index} du fichier A et la clé 'Redshift' de l'objet {$index} du fichier B ne sont pas identiques, comparaison impossible"
                ];
            } else {
                $redshiftComparisonResults[] = [
                    'index' => $index,
                    'message' => "La clé 'Redshift' de l'objet {$index} du fichier A et la clé 'Redshift' de l'objet {$index} du fichier B sont identiques: {$itemA['Redshift']}"
                ];
            }
        }

        // ====================================================================

        // loop the file to count number of json dictionary for each
        // object
        foreach($dataFileA as $index => $item) {
            $dictCountsFileA[] = count($item);
        }

        foreach($dataFileB as $index => $item) {
            $dictCountsFileB[] = count($item);
        }

        // ====================================================================

        return $this->render('index/index.html.twig', [
            'dictCountsFileA' => $dictCountsFileA,
            'dictCountsFileB' => $dictCountsFileB,
            'dataFileA' => $dataFileA,
            'dataFileB' => $dataFileB,
            'redshiftComparisonResults' => $redshiftComparisonResults,
            ]);
    }
}
