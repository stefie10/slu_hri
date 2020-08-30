here=File.dirname(__FILE__)
$tklib_home=File.expand_path("#{here}")
require "#{here}/rakefile.rb"

task :setup do
  mkdir_p($include_build_dir)
  mkdir_p($python_build_dir)
  mkdir_p($jar_build_dir)
  mkdir_p($data_home)
end

task :default => [:setup, :build_carmen, :build]


task :build_carmen do
  carmen = "#{here}/nlp/3rdParty/carmen/carmen"
  sh "cd #{carmen}/src/ && echo -e 'Y\nY\nY\n\n\n8\n' | ./configure -noWerror"
  sh "cd #{carmen}/src && make ECHO=echo"
  sh "cd #{carmen}/src/python && make all ECHO=echo"
end

task :build do
  sh "cd nlp/3rdParty/crf++ && rake setup"
  sh "cd nlp/3rdParty/orange && rake setup"
  sh "cd pytools/gsl_utilities && make"
  sh "cd pytools/spatial_features && make"
  sh "cd cutilities && rake build"
  sh "cd nlp/c_src && make"
  sh "echo \"import nltk; nltk.download('wordnet')\" | rake python"
  sh "echo \"import nltk; nltk.download('punkt')\" | rake python"
  sh "echo \"import nltk; nltk.download('brown')\" | rake python"
  sh "echo \"import nltk; nltk.download('conll2000')\" | rake python"
end

