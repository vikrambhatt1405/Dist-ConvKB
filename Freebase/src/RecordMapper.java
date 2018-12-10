import java.io.IOException;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

public class RecordMapper extends Mapper<Object,Text,Text,Text>{

    @Override
    public void map(Object key, Text value, Context context) throws
            IOException,InterruptedException{
        RecordParser recordParser = new RecordParser();
        String record=value.toString();

        record=recordParser.parse(record);
        Pattern pattern = Pattern.compile("^/m/.*/m/");
        Matcher matcher = pattern.matcher(record);
        if (matcher.find()){
            String subject=record.split("\t")[0];
            String predicate = record.split("\t")[1];
            String object = record.split("\t")[2];
            context.write(new Text(subject+"\t"+object),new Text(predicate));
        }
    }


}
