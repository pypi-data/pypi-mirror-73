import subprocess, pathlib, os, shutil, urllib
from . import Utils

class Engine:
  def preprocess(self,input):
    pass

  def postprocess(self,input):
    pass

  def make_path(self,file):
    return pathlib.Path(file)

  def setup_output_dir(self,input_path,output_path):
    '''
    Setup the output directory for a slideshow, creating
    it if it does not exist.
    .
    If output is None, it will be computed from input.
    '''

    if output_path is None:
      output_path = input_path.parent/input_path.stem

    if not output_path.exists():
      output_path.mkdir()

    return output_path

  def run_cmd(self,cmd,desc=None):
   if desc is None:
     desc = "running:" + " ".join(cmd)
   else:
     print(desc)
   result = subprocess.run(cmd, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
   if result.returncode != 0:
     print(f"There was an error {desc}")
     print(result.stdout.decode('utf-8'))

  def get_images_from_html(self,file):
    if not isinstance(file,pathlib.Path):
      file = pathlib.Path(file)

    parser = Utils.ImageParser()
    parser.feed( file.read_text() )
    return parser.images

  def copy_images_to_output(self,output_path):
    images = self.get_images_from_html(output_path)
    for image in images:
      # don't copy urls
      if urllib.parse.urlparse(str(image)).scheme != "":
        continue
      # don't copy absolute paths
      if image.is_absolute():
        continue

      print(f"copying {str(image)} to {str(output_path.parent)}")
      os.makedirs(output_path.parent/image.parent, exist_ok=True)
      shutil.copyfile(image,output_path.parent/image.parent/image.name)
      




class PandocSlidy(Engine):

  def build(self,input,output=None):

    input = super().make_path(input)
    output_dir = super().setup_output_dir(input,output)
    output = output_dir / "index.html"
    print(f"{input} -> {output}")

    if not (output_dir/"data").exists():
      super().run_cmd(['git','clone', 'https://github.com/slideshow-templates/slideshow-slidy.git',str(output.parent/"data")],"fetching slidy data files")
      shutil.rmtree(str(output.parent/"data/.git"))


    # pandoc options:
    # --self-contained does not work with mathjax
    # --standalone creates a file with header and footer
    # --mathjax uses mathjax javascript to render latex equation. requires an internet connection
    # --to is the format that will be written to
    cmd = list()
    cmd.append("pandoc")
    cmd.append(str(input))
    cmd.append("-o")
    cmd.append(str(output))
    cmd.append("--standalone")
    cmd.append("--mathjax")
    cmd.append("--to")
    cmd.append("slidy")
    cmd.append("--css")
    cmd.append("slidy_extra.css")
    cmd.append("--variable")
    cmd.append("slidy-url=./data")

    super().run_cmd(cmd,"building the slides.")

    super().copy_images_to_output(output)


  
class PandocPowerPoint(Engine):

  def build(self,input,output=None):

    input = super().make_path(input)
    output_dir = super().setup_output_dir(input,output)
    output = output_dir / (str(input.stem)+".pptx")
    print(f"{input} -> {output}")

    template_file = pathlib.Path("mdSlides-template.pptx")

    cmd = list()
    cmd.append("pandoc")
    cmd.append(str(input))
    cmd.append("-o")
    cmd.append(str(output))
    if template_file.exists():
      cmd.append("--reference-doc")
      cmd.append(str(template_file))

    super().run_cmd(cmd,"building the slides.")
