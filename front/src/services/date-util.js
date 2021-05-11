export default class DateUtil {

    static format(d) {
        return new Date(d).toGMTString()
    }

    static formatDiffNow(d) {
        let ms_min = 60 * 1000;
        let ms_hour = ms_min * 60;
        let ms_day = ms_hour * 24;
        let ms_month = ms_day * 30;
        let ms_year = ms_month * 365;

        let dateNow = new Date();
        let dateBefore = new Date(d);
        let diff = dateNow - dateBefore;

        if (diff < ms_min) {
            return Math.round(diff / 1000) + ' seconds ago';
        } else if (diff < ms_hour) {
            return Math.round(diff / ms_min) + ' minutes ago';
        } else if (diff < ms_day) {
            return Math.round(diff / ms_hour) + ' hours ago';
        } else if (diff < ms_month) {
            return Math.round(diff / ms_day) + ' days ago';
        } else if (diff < ms_year) {
            return Math.round(diff / ms_month) + ' months ago';
        } else {
            return Math.round(diff / ms_year) + ' years ago';
        }


    }
}