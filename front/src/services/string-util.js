export default class StringUtil {
    static formatDn(dn) {
        if (dn.length > 16) {
            return dn.slice(0, 14) + '...'
        } else {
            return dn
        }
    }
}