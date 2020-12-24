use anyhow::Result;
use structopt::StructOpt;

fn parse_cups(cups: &str) -> Result<Vec<u32>> {
    const RADIX: u32 = 10;
    Ok(cups
        .chars()
        .map(|c| c.to_digit(RADIX).expect("Could not parse char"))
        .collect())
}

fn play_n_moves(cups: &mut Vec<u32>, n: u32) -> Result<()> {
    let min_cup: u32 = *cups.iter().min().expect("Could not find min");
    let max_cup: u32 = *cups.iter().max().expect("Could not find max");
    let mut current_index = 0;
    for _ in 0..n {
        let mut removed = Vec::<u32>::new();
        for __ in 0..3 {
            let remove_index = (current_index + 1) % cups.len();
            if remove_index < current_index {
                current_index -= 1;
            }
            removed.push(cups.remove(remove_index));
        }
        let mut dest_cup = cups[current_index] - 1;
        loop {
            if dest_cup < min_cup {
                dest_cup = max_cup;
            }
            if !removed.contains(&dest_cup) {
                break;
            }
            dest_cup -= 1;
        }
        let dest_index = cups
            .iter()
            .position(|&c| c == dest_cup)
            .expect("Could not find destination cup");
        let insert_index = (dest_index + 1) % cups.len();
        if insert_index <= current_index {
            current_index += removed.len();
        }
        for cup in removed.iter().rev() {
            cups.insert(insert_index, *cup);
        }
        current_index = (current_index + 1) % cups.len();
    }
    Ok(())
}

fn play_n_easy_moves(mut cups: Vec<u32>, n: u32) -> Result<String> {
    play_n_moves(&mut cups, n)?;
    let one_index = cups
        .iter()
        .position(|&c| c == 1)
        .expect("Could not find cup 1");
    let mut part_one: Vec<&u32> = cups.iter().skip(one_index + 1).collect();
    let part_two = cups.iter().take(one_index);
    part_one.extend(part_two);
    Ok(part_one
        .iter()
        .map(|c| c.to_string())
        .collect::<Vec<String>>()
        .join(""))
}

fn play_n_hard_moves(mut cups: Vec<u32>, n: u32) -> Result<String> {
    let max_cup: u32 = *cups.iter().max().expect("Could not find max");
    cups.extend((max_cup + 1)..=1000000);
    play_n_moves(&mut cups, n)?;
    let one_index = cups
        .iter()
        .position(|&c| c == 1)
        .expect("Could not find cup 1");
    let value_one = cups[(one_index + 1) % cups.len()];
    let value_two = cups[(one_index + 2) % cups.len()];
    Ok((value_one * value_two).to_string())
}

#[derive(Debug, StructOpt)]
pub struct Flags {
    #[structopt(short = "n", long = "next")]
    pub next: bool,
}

fn main() -> Result<()> {
    let flags = Flags::from_args();
    let cups = parse_cups("685974213");
    if flags.next {
        println!("{}", play_n_hard_moves(cups?, 10000000)?);
    } else {
        println!("{}", play_n_easy_moves(cups?, 100)?);
    }
    Ok(())
}

#[cfg(test)]
mod tests {
    use crate::{parse_cups, play_n_easy_moves, play_n_hard_moves};

    #[test]
    fn test_play_ten_easy_moves() {
        assert_eq!(
            play_n_easy_moves(parse_cups("389125467").unwrap(), 10).unwrap(),
            "92658374"
        );
    }

    #[test]
    fn test_play_hundred_easy_moves() {
        assert_eq!(
            play_n_easy_moves(parse_cups("389125467").unwrap(), 100).unwrap(),
            "67384529"
        );
    }

    #[test]
    fn test_play_n_hard_moves() {
        assert_eq!(
            play_n_hard_moves(parse_cups("389125467").unwrap(), 10000000).unwrap(),
            "149245887792"
        );
    }
}
