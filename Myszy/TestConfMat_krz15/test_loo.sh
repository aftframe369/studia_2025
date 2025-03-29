#!/bin/bash
for i in t_*.csv
do
  ii="${i:2}"
  iii="${ii%.csv}"
  ./MzExtractSingleClassifier "t_${iii}_oolda.txt" other#tumour#8D temp_classifier.txt
  ./MzPredict -c temp_classifier.txt -i "$i" -v >> "test_oolda8D.txt"
  ./MzExtractSingleClassifier "t_${iii}_oolda.txt" other#tumour#7D temp_classifier.txt
  ./MzPredict -c temp_classifier.txt -i "$i" -v >> "test_oolda7D.txt"
  ./MzExtractSingleClassifier "t_${iii}_oolda.txt" other#tumour#6D temp_classifier.txt
  ./MzPredict -c temp_classifier.txt -i "$i" -v >> "test_oolda6D.txt"
  ./MzExtractSingleClassifier "t_${iii}_oovsch.txt" tumour#6D temp_classifier.txt
  ./MzPredict -c temp_classifier.txt -i "$i" -v >> "test_oovsch6D.txt"
  ./MzExtractSingleClassifier "t_${iii}_oovsch.txt" tumour#5D temp_classifier.txt
  ./MzPredict -c temp_classifier.txt -i "$i" -v >> "test_oovsch5D.txt"
  ./MzExtractSingleClassifier "t_${iii}_oovsch.txt" tumour#4D temp_classifier.txt
  ./MzPredict -c temp_classifier.txt -i "$i" -v >> "test_oovsch4D.txt"
  ./MzPredict -c "t_${iii}_oosvm.txt" -i "$i" -v >> "test_oosvm400D.txt"
done

