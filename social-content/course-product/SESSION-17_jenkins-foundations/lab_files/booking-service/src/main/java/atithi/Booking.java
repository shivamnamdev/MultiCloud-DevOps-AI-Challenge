package atithi;

import java.time.LocalDate;
import java.time.temporal.ChronoUnit;

public class Booking {
    /** Number of nights between check-in and check-out. */
    public static long nights(LocalDate checkIn, LocalDate checkOut) {
        if (!checkOut.isAfter(checkIn)) {
            throw new IllegalArgumentException("check-out must be after check-in");
        }
        return ChronoUnit.DAYS.between(checkIn, checkOut);
    }

    public static void main(String[] args) {
        System.out.println("nights=" + nights(LocalDate.of(2026, 12, 1), LocalDate.of(2026, 12, 4)));
    }
}
