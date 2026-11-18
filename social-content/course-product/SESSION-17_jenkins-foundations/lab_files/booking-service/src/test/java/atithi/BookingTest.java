package atithi;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.time.LocalDate;
import org.junit.jupiter.api.Test;

class BookingTest {
    @Test
    void threeNights() {
        assertEquals(3, Booking.nights(LocalDate.of(2026, 12, 1), LocalDate.of(2026, 12, 4)));
    }

    @Test
    void checkOutBeforeCheckInIsRejected() {
        assertThrows(IllegalArgumentException.class,
            () -> Booking.nights(LocalDate.of(2026, 12, 4), LocalDate.of(2026, 12, 1)));
    }
}
