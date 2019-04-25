$exampleDir="D:\Materials\Python\djangoProject\solr-4.10.4\example"

If ( Test-Path "$exampleDir\blog" ) { Remove-Item "$exampleDir\blog" } 

New-Item -Path $exampleDir -Name "blog" -ItemType "directory"
New-Item -Path "$exampleDir/blog" -Name "data" -ItemType "directory"
New-Item -Path "$exampleDir/blog" -Name "conf" -ItemType "directory"
New-Item -Path "$exampleDir/blog/conf" -Name "protwords.txt" -ItemType "file"
New-Item -Path "$exampleDir/blog/conf" -Name "schema.xml" -ItemType "file"
New-Item -Path "$exampleDir/blog/conf" -Name "solrconfig.xml" -ItemType "file"
New-Item -Path "$exampleDir/blog/conf" -Name "stopwords.txt" -ItemType "file"
New-Item -Path "$exampleDir/blog/conf" -Name "synonyms.txt" -ItemType "file"
New-Item -Path "$exampleDir/blog/conf" -Name "lang" -ItemType "directory"
New-Item -Path "$exampleDir/blog/conf/lang" -Name "stopwords_en.txt" -ItemType "file"




