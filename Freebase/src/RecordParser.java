public class RecordParser {
    public String parse(String record) {

        record = record.replaceAll(">", "");
        record = record.replaceAll("<", "");
        record = record.replaceAll("http://rdf\\.freebase\\.com/ns", "");
        record = record.replaceAll("http://www\\.w3\\.org/[0-9]*/[0-9]*/[0-9]*-*", "");
        record = record.replaceAll("\t.$", "");
        record = record.replaceAll("\\.","/");
        return record;
    }
}
