#!/bin/bash
for i in t_*.csv
do
  ii="${i:2}"
  iii="${ii%.csv}"
  ./MzExtractSingleClassifier "t_${iii}_ddlda.txt" other#tumour#8D temp_classifier.txt
  ./MzPredict -c temp_classifier.txt -i "$i" -v >> "test_ddlda8D.txt"
  ./MzExtractSingleClassifier "t_${iii}_ddlda.txt" other#tumour#7D temp_classifier.txt
  ./MzPredict -c temp_classifier.txt -i "$i" -v >> "test_ddlda7D.txt"
  ./MzExtractSingleClassifier "t_${iii}_ddlda.txt" other#tumour#6D temp_classifier.txt
  ./MzPredict -c temp_classifier.txt -i "$i" -v >> "test_ddlda6D.txt"
  ./MzExtractSingleClassifier "t_${iii}_ddvsch.txt" tumour#6D temp_classifier.txt
  ./MzPredict -c temp_classifier.txt -i "$i" -v >> "test_ddvsch6D.txt"
  ./MzExtractSingleClassifier "t_${iii}_ddvsch.txt" tumour#5D temp_classifier.txt
  ./MzPredict -c temp_classifier.txt -i "$i" -v >> "test_ddvsch5D.txt"
  ./MzExtractSingleClassifier "t_${iii}_ddvsch.txt" tumour#4D temp_classifier.txt
  ./MzPredict -c temp_classifier.txt -i "$i" -v >> "test_ddvsch4D.txt"
  ./MzPredict -c "t_${iii}_ddsvm.txt" -i "$i" -v >> "test_ddsvm400D.txt"
done

