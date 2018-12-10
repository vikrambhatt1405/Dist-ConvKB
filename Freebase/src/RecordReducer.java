import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

import java.io.IOException;

public class RecordReducer extends Reducer<Text,Text,Text,Text> {
    @Override
    public void reduce(Text key,Iterable<Text> values,Context context) throws IOException,InterruptedException{
        String finalValue="";
        Boolean flag = true;
        for(Text text:values) {
            if (flag) {
                finalValue = text.toString();
                flag = false;
            } else {
                finalValue = finalValue.concat("." + text.toString());
            }
        }
        String subject=key.toString().split("\t")[0];
        String object=key.toString().split("\t")[1];
        finalValue = subject+"\t"+finalValue+"\t"+object;
        context.write(new Text(finalValue),new Text(""));
    }
}

