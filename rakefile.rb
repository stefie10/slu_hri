ENV['TKLIB_HOME'] = $tklib_home
$agile_home="#{$tklib_home}/../agile/"
ENV['AGILE_HOME'] = $agile_home

$python_version = `python -c "import sys; sys.stdout.write(sys.version[:3])"`

$python_build_dir = "#{$tklib_home}/build/lib/python#{$python_version}"
$pbd = $python_build_dir

$python_build_dir = "#{$tklib_home}/build/lib/python#{$python_version}"
$jar_build_dir = "#{$tklib_home}/build/share/java"
$data_home = "#{$tklib_home}/build/data/"

directory $python_build_dir

$lib_build_dir = "#{$tklib_home}/build/lib/"
directory $lib_build_dir

$include_build_dir = "#{$tklib_home}/build/include/"
directory $include_build_dir

ENV['PYTHONPATH'] = ["#{$python_build_dir}",
                     "#{$tklib_home}/build/lib/python",
                     "#{$tklib_home}/pytools/map_partitioning/src/",
                     "#{$tklib_home}/cutilities/python/",
                     "#{$tklib_home}/cutilities/python/",
                     `cd #{$tklib_home}/nlp && rake -s pythonpath`.chomp,
                     ENV['PYTHONPATH']].join(":")
ENV['JAVA_LIB'] = "#{$tklib_home}/java/slu-java/share/java/"
ENV['DATA_HOME'] = $data_home
ENV['CLASSPATH']  = ["#{$tklib_home}/build/share/java/stanford-ner-2009-01-16.jar",
                     FileList["#{$tklib_home}/build/share/java/*.jar"].join(":")].join(":")
                     

ENV['LD_LIBRARY_PATH'] = [`cd #{$tklib_home}/nlp && rake -s ldlibrarypath`.chomp,
                          $lib_build_dir
                         ].join(":")
$forklift_home = "#{$tklib_home}/pytools/forklift"
ENV['FORKLIFT_HOME'] = $forklift_home
ENV['ARKREF_HOME']="#{$tklib_home}/build/share/java/arkref"

$pdb_python = (ENV['PDB_PYTHON'] or false)
$debug_python = (ENV['DEBUG_PYTHON'] or false)
$valgrind_python = (ENV['VALGRIND_PYTHON'] or false)
$memprof_python = (ENV['MEMPROF_PYTHON'] or false)
$efence_python = (ENV['EFENCE_PYTHON'] or false)

DEFAULT_CFLAGS="-I#{$include_build_dir} " + 
  "-I/usr/include/python#{$python_version}"
DEFAULT_LDFLAGS="-L#{$include_lib_dir} " + 
  "-I/usr/include/python#{$python_version}"

def make_lib_targets(target_name, name, c_files, ldflags, dest)
  o_files = []
  c_files.each do |src|
    target = File.join(File.dirname(src),
                       File.basename(File.basename(src, ".c"), ".cxx") + '.o')
    o_files.push(target)
  end
  file name => o_files do |t|
    sh "g++ -shared -o #{name} #{o_files.join(' ')} -L#{$lib_build_dir} #{ldflags}"
  end
  task target_name => [name]
  make_copy_targets(target_name, [name], dest)
end

def make_swig_targets(files, deps, libname, cflags, ldflags)
  cxx_files = []
  py_files = []
  files.each do |src|
    cxx_target = File.join(File.dirname(src),
                           File.basename(src, ".i") + '_wrap.cxx')
    o_target = File.join(File.dirname(src),
                         File.basename(src, ".i") + '_wrap.o')
    py_target = File.join(File.dirname(src),
                          File.basename(src, ".i") + '.py')

    file cxx_target => [src] + deps do |t|
      sh "swig -c++ #{DEFAULT_CFLAGS} #{cflags} -python -keyword -w511 -threads #{src}"
    end
    cxx_files.push(cxx_target)
    py_files.push(py_target)
  end
  make_o_targets(:build_swig, cxx_files, ".cxx", cflags)
  make_lib_targets(:build_swig, libname, cxx_files, ldflags, $pbd)
  make_copy_targets(:build_swig, py_files, $pbd)
  task :build_swig => [libname]
end

def make_copy_targets(target_name, source_files, dest_dir)
   source_files.each do |src|
 
    target = File.join(dest_dir, File.basename(src))
    file target => [src] do
      mkdir_p(File.dirname(target))
      sh "cp #{src} #{target}"
    end
    task target_name => [target]
    puts "making target for: #{target_name} #{target}\n"
  end
end

def make_o_targets(target_name, source_files, ext, cflags)
   source_files.each do |src|
     target = File.join(File.dirname(src),
                        File.basename(src, ext) + '.o')
     file  target => [src] do |t|
       sh "g++ -c -g #{cflags} -fPIC  #{DEFAULT_CFLAGS} -o #{target} #{src}"
     end
     task target_name => [target]
   end
 end
def python(file)
  puts ENV['PYTHONPATH'] 
  puts "\n"
  if ($debug_python)
    sh "gdb --args python #{file}"
  elsif  ($valgrind_python)
    sh "valgrind --tool=memcheck --suppressions=#{$tklib_home}/etc/valgrind-python.supp  --suppressions=#{$tklib_home}/etc/valgrind-java.supp python -u #{file}"         
  elsif ($memprof_python)
    sh "memprof /usr/bin/python #{file}"
  elsif ($pdb_python)
    sh "pdb #{file}"
  elsif ($efence_python)
    sh "export LD_PRELOAD=libefence.so.0.0 && gdb --args python #{file}"
  else
    sh "time python #{file}"
  end
end


task :buildGui
FileList['python/*.ui', 'python/**/*.ui'].each do |src|
  target = File.join(File.dirname(src),
                     File.basename(src, ".ui") + '_ui.py')
  file  target => [src] do |t|
    sh "pyuic4 #{t.prerequisites} -o #{t.name}\n"

  end
  task :buildGui => [target]
end



def make_python_targets(target_name, python_files)
  python_files.each do |source|
    target = $python_build_dir + "/" + source.split("python/")[1..-1].join("/")
    file target => source do
      mkdir_p(File.dirname(target))
      cp source, target, :verbose=>true
    end
    task target_name => target
  end
end



def make_class_targets(target_name, source_files)
   source_files.each do |src|
     target = File.join(File.dirname(src),
                        File.basename(src, ".java") + ".class")
     file  target => [src] do |t|
      sh "javac -classpath #{ENV['CLASSPATH']} #{$java_build_dir} " + 
        "-sourcepath java -d java #{source_files}"
     end
     task target_name => [target]
   end
 end


def make_jar_target(jar_name)
  task :build_java => [jar_name]
  file jar_name do
    sh "cd java && jar cf #{jar_name} . && mv #{jar_name} #{$jar_build_dir}"
  end

end


task :clean_python do
  rm_rf $python_build_dir, :verbose=>true
end


desc "Run the test cases."
task :tests => [:everything] do
  sh "/usr/bin/nosetests `find python -name '*_test.py'`"
end

desc "Print the python path"
task :pythonpath do
  puts ENV["PYTHONPATH"]
end



task :python do
  sh "python"
end

task :default => :all

task :everything do
  sh "cd #{$tklib_home} && make all"
end


def python_task(*args, &block)
  if args.last.is_a?(Hash)
    key, value = args.last.map { |k, v| [k,v] }.first
    args.last[key] += [:everything]
  else
    args = [{args.first => [:everything]}]
  end
  Rake::Task.define_task(*args, &block)
end
