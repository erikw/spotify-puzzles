import java.util.Random;

/**
* @author Tommy Ivarsson
*/

public class InputGenerator {

	public static void main(String[] args) {
		int nbrTests = 100;
		System.out.println(nbrTests);

		int cats;
		int dogs;
		int voters;

		Random rand = new Random();
		for(int i = 0; i < nbrTests; i++) {
			cats = randomBetween(1, 100);
			dogs = randomBetween(1, 100);
			voters = randomBetween(0, 500);
			System.out.println(cats + " " + dogs + " " + voters);

			for (int j = 0; j < voters; j++) {
				if (randomBetween(0, 2) == 1) {
					System.out.println("D" + randomBetween(1, dogs) + " " + "C" + randomBetween(1, cats));
				} else {
					System.out.println("C" + randomBetween(1, cats) + " " + "D" + randomBetween(1, dogs));
				}
			}
		}
	}

	private static int randomBetween(int low, int high) {
		return high-low >= 1 ? new Random().nextInt(high-low) + low : low;
	}
}

