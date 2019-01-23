import java.io.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.zip.GZIPInputStream;
public class Main {

    public static void main(String[] args) throws IOException {

        String filename = "/home/vikrambhatt/ExternalStorage/freebase-rdf-latest.gz";
        InputStream fileStream = new FileInputStream(filename);
        InputStream gzipStream = new GZIPInputStream(fileStream);
        Reader decoder = new InputStreamReader(gzipStream);
        BufferedReader buffered = new BufferedReader(decoder);
        String content;
        RecordParser recordParser = new RecordParser();
        Pattern pattern = Pattern.compile("^/m/.*/m/");
        while ((content = buffered.readLine()) != null) {
            content = recordParser.parse(content);
            //System.out.println(content);
            Matcher matcher = pattern.matcher(content);
            if (matcher.find()) {

                System.out.println(content.split("\t")[0]);
            }
            matcher.reset(content);
        }
    }
}
